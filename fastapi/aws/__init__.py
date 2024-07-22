import boto3

def init_app(app):
    aws_session = boto3.session.Session(
        aws_access_key_id=app.state.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=app.state.config['AWS_SECRET_KEY'],
        region_name=app.state.config['AWS_REGION'])

    if not app.state.config.get('AWS_LOGGROUP_NAME'):
        print('Lack AWS configuration keys, ignore AWS CloudWatch log handlers')
        return

    return aws_session
