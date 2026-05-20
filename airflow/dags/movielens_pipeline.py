
from airflow import DAG
from datetime import datetime
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.operators.bash import BashOperator

from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

dag = DAG(
    dag_id='movielens_pipeline',
    start_date=datetime(2026,5,19),
    schedule='@daily', # run every day 
    catchup = False, # don't backfill missed runs
)


################################ TASK 1: Check S3 Files


check_s3_files = S3KeySensor(
    task_id = 'check_s3_files',
    bucket_name = 'netflix-bucket-01', # S3 bucket name
    bucket_key=[     #  fileS to check for
            'ratings.csv',
            'movies.csv',
            'genome-scores.csv',
            'genome-tags.csv',
            'links.csv',
            'tags.csv'
        ],
    aws_conn_id = 'aws_conn', # connection set in Airflow UI
    poke_interval = 60, #check every 60 seconds
    timeout = 120,  #give up after 2 minutes (120 seconds)
    dag=dag
    ) 




################################ TASK 2: Load S3 to Snowflake RAW



COPY_SQL = '''

        USE ROLE TRANSFORM;
        USE WAREHOUSE COMPUTE_WH;
        USE DATABASE NETFLIX_DB;
        USE SCHEMA RAW;

        
  

        COPY INTO raw_movies
        FROM '@NETFLIX_DB.RAW.NETFLIXSTAGE/movies.csv'
        FILE_FORMAT = (TYPE = 'CSV' SKIP_HEADER = 1 FIELD_OPTIONALLY_ENCLOSED_BY = '"');
    

        COPY INTO raw_ratings
        FROM '@NETFLIX_DB.RAW.NETFLIXSTAGE/ratings.csv'
        FILE_FORMAT = (TYPE = 'CSV' SKIP_HEADER = 1 FIELD_OPTIONALLY_ENCLOSED_BY = '"');


        COPY INTO raw_tags
        FROM '@NETFLIX_DB.RAW.NETFLIXSTAGE/tags.csv'
        FILE_FORMAT = (TYPE = 'CSV' SKIP_HEADER = 1 FIELD_OPTIONALLY_ENCLOSED_BY = '"');


        COPY INTO raw_genome_scores
        FROM '@NETFLIX_DB.RAW.NETFLIXSTAGE/genome-scores.csv'
        FILE_FORMAT = (TYPE = 'CSV' SKIP_HEADER = 1 FIELD_OPTIONALLY_ENCLOSED_BY = '"');


        COPY INTO raw_genome_tags
        FROM '@NETFLIX_DB.RAW.NETFLIXSTAGE/genome-tags.csv'
        FILE_FORMAT = (TYPE = 'CSV' SKIP_HEADER = 1 FIELD_OPTIONALLY_ENCLOSED_BY = '"');


        COPY INTO raw_links
        FROM '@NETFLIX_DB.RAW.NETFLIXSTAGE/links.csv'
        FILE_FORMAT = (TYPE = 'CSV' SKIP_HEADER = 1 FIELD_OPTIONALLY_ENCLOSED_BY = '"');

        '''


# And change the operator:
load_to_snowflake = SQLExecuteQueryOperator(
    task_id          = 'load_to_snowflake',
    sql              = COPY_SQL,
    conn_id          = 'snowflake_conn',   # 
    dag              = dag
)





################################ TASK 3: dbt Run: Staging Models (staging)

#   This builds in Snowflake STAGING schema:
# src_movies (view)
# src_ratings (view)
# src_tags (view)
# src_genome_score (view)
# src_genome_tags (view)
# src_links (view)


DBT_PROJECT_DIR = '/opt/airflow/dbt_project'

dbt_run_staging = BashOperator(
    task_id = 'dbt_run_staging',
    bash_command = f'''
        cd {DBT_PROJECT_DIR} &&
        dbt deps &&
        dbt run --select staging --profiles-dir {DBT_PROJECT_DIR}
        ''',
    dag=dag
)






################################ TASK 4: dbt Run: Core Models (dim,fact,bridge)

#   This builds in Snowflake ANALYTICS schema:
# dim_movies (table) 
# dim_users (table)
# dim_genome_tags (table) 
# fct_ratings (incremental table) 
# bridge_movie_tags (table) 

dbt_run_core = BashOperator(
    task_id = 'dbt_run_core',
    bash_command = f'''
        cd {DBT_PROJECT_DIR} &&
        dbt run --select dim fct bridge --profiles-dir {DBT_PROJECT_DIR}
        ''',
    dag=dag
    )




################################ TASK 5: dbt Run: Mart Models 

#   This builds in Snowflake ANALYTICS schema:
# mart_genre_summary (table)
# mart_movie_releases (table) 
# mart_top_movies (table)

dbt_run_marts = BashOperator(
    task_id = 'dbt_run_marts',
    bash_command = f'''
        cd {DBT_PROJECT_DIR} &&
        dbt run --select mart --profiles-dir {DBT_PROJECT_DIR}
        ''',
    dag=dag
)




################################ TASK 6: dbt Test

# Tests that will run (from schema.yml):
# unique + not_null on all surrogate keys 
# unique + not_null on natural keys (movie_id, user_id, tag_id)
# relationships: fct_ratings.movie_id -> dim_movies.movie_id
# relationships: fct_ratings.user_id -> dim_users.user_id
# accepted_values: fct_ratings.rating in [0.5, 1.0, 1.5...5.0]
# not_null on bridge_movie_tags columns

dbt_test = BashOperator(
    task_id = 'dbt_test',
    bash_command = f'''
        cd {DBT_PROJECT_DIR} &&
        dbt test --profiles-dir {DBT_PROJECT_DIR}
        ''',
    dag=dag
)




################################# DEPENDENCY CHAIN 
check_s3_files >> load_to_snowflake >> dbt_run_staging >> dbt_run_core >> dbt_run_marts >> dbt_test