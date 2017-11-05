import boto3

# Get the service resource
sqs = boto3.resource('sqs')

# Get the queue
queue = sqs.get_queue_by_name(QueueName='Weather.fifo')

for i in range(30):
    data = {'Last': {'Temp': '24.1', 'Time': '2017-11-04 14:12:22', 'Hum': '29.1'}, \
            'Avg': {'Temp': '23.93', 'Time': '2017-11-04 14:12:22', 'Hum': '28.73'}, \
            'Min': {'Temp': '21.8', 'Time': '2017-11-04 14:12:22', 'Hum': '26.2'}, \
            'Max': {'Temp': '24.1', 'Time': '2017-11-04 14:12:22', 'Hum': '29.1'}, \
            'Unit': 'C'}
    response = queue.send_message(
        MessageBody=str(data),
        MessageGroupId='messageGroup1'
    )
    # The response is NOT a resource, but gives you a message ID and MD5
    print(response.get('MessageId'))
    print(response.get('MD5OfMessageBody'))
