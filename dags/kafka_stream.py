# import uuid
from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator

default_args = {
    'owner': 'airscholar',
    'start_date': datetime(2023, 9, 3, 10, 00),
    'catchup': False,
    'retry_delay': timedelta(minutes=1),
    'retries': 1
}

@dag(default_args=default_args)
def user_registry():
    
    @task
    def get_data():
        import requests
        url = 'https://randomuser.me/api/'
        rawData = requests.get(url).json()
        data = rawData['results'][0]
        return data
    
    @task
    def format_data(res):
        data = {}
        location = res['location']
        # data['id'] = str(uuid.uuid4())
        data['first_name'] = res['name']['first']
        data['last_name'] = res['name']['last']
        data['gender'] = res['gender']
        data['address'] = f"{str(location['street']['number'])} {location['street']['name']}, " \
                        f"{location['city']}, {location['state']}, {location['country']}"
        data['post_code'] = location['postcode']
        data['email'] = res['email']
        data['username'] = res['login']['username']
        data['dob'] = res['dob']['date']
        data['registered_date'] = res['registered']['date']
        data['phone'] = res['phone']
        data['picture'] = res['picture']['medium']
        return data

    @task
    def process_male_data(data):
        data['business_email'] = f"{data['email'].split('@')[0]}@newSet.nig"
        data['userCompany'] = f"{data['username']}@newSet"
        data['id'] = f"{data['phone']}-0"
        return data

    @task
    def process_female_data(data):
        data['business_email'] = f"{data['email'].split('@')[0]}@newSet.wom"
        data['userCompany'] = f"{data['username']}@newSet"
        data['id'] = f"{data['phone']}-1"
        return data

    @task.branch
    def branch_by_gender(data):
        gender = data['gender']
        if gender == 'male':
            return 'process_male_data'
        elif gender == 'female':
            return 'process_female_data'
        else:
            return 'unknown_gender'

    @task
    def stream_to_kafka(data):
        import json
        from kafka import KafkaProducer
        import time
        import logging

        producer = KafkaProducer(bootstrap_servers=['broker:29092'], max_block_ms=5000)
        curr_time = time.time()

        try:
            # Send the processed data to Kafka
            producer.send('users_created', json.dumps(data).encode('utf-8'))
            producer.flush()  # Ensure the message is sent
            logging.info(f"Successfully sent data for user: {data.get('username')}")
        except Exception as e:
            logging.error(f'An error occurred while sending to Kafka: {e}')
            raise  # Re-raise the exception to trigger retry

        # Sleep for remainder of minute if needed
        elapsed_time = time.time() - curr_time
        if elapsed_time < 60:
            time.sleep(60 - elapsed_time)
        
        return data

    # Define tasks
    start = EmptyOperator(task_id='start')
    unknown_gender = EmptyOperator(task_id='unknown_gender')
    end = EmptyOperator(
        task_id='end',
        trigger_rule='none_failed_min_one_success'
    )

    # Get and format data
    raw_data = get_data()
    formatted_data = format_data(raw_data)

    # Set up the task dependencies
    start >> formatted_data
    
    # Branch based on gender
    branch_task = branch_by_gender(formatted_data)
    formatted_data >> branch_task

    # Process data based on gender
    male_processed = process_male_data(formatted_data)
    female_processed = process_female_data(formatted_data)

    # Stream processed data to Kafka
    male_streamed = stream_to_kafka(male_processed)
    female_streamed = stream_to_kafka(female_processed)

    # Set up branch paths including Kafka streaming
    branch_task >> [male_processed, female_processed, unknown_gender]
    male_processed >> male_streamed
    female_processed >> female_streamed
    [male_streamed, female_streamed, unknown_gender] >> end

user_registry()
