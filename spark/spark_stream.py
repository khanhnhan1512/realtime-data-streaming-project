import logging
import sys
from datetime import datetime

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructField, StructType, StringType


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/tmp/spark_streaming.log')
    ]
)

logger = logging.getLogger(__name__)

def create_keyspace(session):
    """
    Create a keyspace in Cassandra if it doesn't exist.
    """
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS spark_streams
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};
    """)
    logger.info("Keyspace 'spark_streams' created successfully.")
    print("Keyspace 'spark_streams' created successfully.")


def create_table(session):
    """
    Create a table in Cassandra if it doesn't exist.
    """
    session.execute("""
    CREATE TABLE IF NOT EXISTS spark_streams.users_created (
        id UUID PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        gender TEXT,
        address TEXT,
        postcode TEXT,
        email TEXT,
        username TEXT,
        dob TEXT,
        registered_date TEXT,
        phone TEXT,
        picture TEXT
        );
    """)
    logger.info("Table 'users_created' created successfully.")
    print("Table 'users_created' created successfully.")  # Backup logging


def create_spark_connection():
    """
    Create and return a Spark session.
    """
    spark_conn = None
    try:
        # spark_conn = SparkSession.builder.appName("SparkDataStreaming")\
        #     .config("spark.jars.packages", "com.datastax.spark:spark-cassandra-connector_2.13:jar:3.5.1, org.apache.spark:spark-sql-kafka-0-10_2.13:jar:3.5.1")\
        #     .config("spark.cassandra.connection.host", "localhost")\
        #     .getOrCreate() # Need to download these files and add them to `.venv/lib/python<version>/site-packages/pyspark/jars/`

        spark_conn = SparkSession.builder.appName("SparkDataStreaming") \
            .config("spark.cassandra.connection.host", "cassandra_db") \
            .getOrCreate()
        
        spark_conn.sparkContext.setLogLevel("ERROR")
        logger.info("Spark session created successfully.")
        print("Spark session created successfully.")
    except Exception as e:
        logger.error(f"Error creating Spark session: {e}")
        print(f"Error creating Spark session: {e}")
    
    return spark_conn

def connect_to_kafka(spark_conn):
    """
    Connect to Kafka and return a streaming DataFrame.
    """
    spark_df = None
    try:
        spark_df = spark_conn.readStream.format('kafka')\
            .option('kafka.bootstrap.servers', 'broker:29092')\
            .option('subscribe', 'users_created')\
            .option('startingOffsets', 'earliest')\
            .load()
        logger.info("Kafka dataframe created successfully.")
        print("Kafka dataframe created successfully.")
    except Exception as e:
        logger.warning(f"Kafka dataframe could not be created: {e}")
        print(f"Kafka dataframe could not be created: {e}")
    return spark_df

def create_cassandra_connection():
    """
    Create and return a Cassandra session.
    """
    cass_session = None
    try:
        cluster = Cluster(['cassandra_db'])
        cass_session = cluster.connect()
        logger.info("Cassandra session created successfully.")
        print("Cassandra session created successfully.")
    except Exception as e:
        logger.error(f"Could not create cassandra connection: {e}")
        print(f"Could not create cassandra connection: {e}")
    return cass_session

def create_selection_df_from_kafka(spark_df):
    """
    Create a selection DataFrame from the Kafka DataFrame.
    """
    schema = StructType([
        StructField("id", StringType(), False),
        StructField("first_name", StringType(), False),
        StructField("last_name", StringType(), False),
        StructField("gender", StringType(), False),
        StructField("address", StringType(), False),
        StructField("postcode", StringType(), False),
        StructField("email", StringType(), False),
        StructField("username", StringType(), False),
        StructField("dob", StringType(), False),
        StructField("registered_date", StringType(), False),
        StructField("phone", StringType(), False),
        StructField("picture", StringType(), False)
    ])

    sel = spark_df.selectExpr("CAST(value AS STRING)")\
        .select(from_json(col('value'), schema).alias('data')).select('data.*')
    logger.info(f"Selection dataframe created successfully")
    print("Selection dataframe created successfully")  # Backup logging
    return sel

if __name__ == '__main__':
    print("=== Starting Spark Streaming Application ===")
    logger.info("=== Starting Spark Streaming Application ===")
    spark_conn = create_spark_connection()
    if spark_conn:
        # connect to kafka with spark connection
        spark_df = connect_to_kafka(spark_conn)
        selection_df = create_selection_df_from_kafka(spark_df)
        cass_session = create_cassandra_connection()
        if cass_session:
            create_keyspace(cass_session)
            create_table(cass_session)

            logger.info("Streaming is being started...")
            print("Streaming is being started...")

            streaming_query = (selection_df.writeStream.format("org.apache.spark.sql.cassandra").option('checkpointLocation', '/tmp/checkpoint').option('keyspace', 'spark_streams').option('table', 'users_created').start())

            streaming_query.awaitTermination()

