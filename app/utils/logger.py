import logging
import watchtower
import boto3
from app.core.config import settings

def setup_cloudwatch_logging():
    logger = logging.getLogger()
    logger.setLevel(settings.LOG_LEVEL)

    # AWS CloudWatch Handler
    cw_handler = watchtower.CloudWatchLogHandler(
        log_group=settings.CLOUDWATCH_LOG_GROUP,
        boto3_client=boto3.client("logs", region_name=settings.AWS_REGION)
    )
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    cw_handler.setFormatter(formatter)
    
    logger.addHandler(cw_handler)
    
    # Also log to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

class MetricsService:
    def __init__(self):
        self.cw_metrics = boto3.client('cloudwatch', region_name=settings.AWS_REGION)

    def put_metric(self, name: str, value: float, unit: str = 'Count'):
        self.cw_metrics.put_metric_data(
            Namespace='LLMOpsProject',
            MetricData=[
                {
                    'MetricName': name,
                    'Value': value,
                    'Unit': unit
                }
            ]
        )
