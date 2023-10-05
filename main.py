from prometheus_client import start_wsgi_server, CollectorRegistry, Gauge
import os
import threading
import time
import random
import re

import nextcloud

HTTP_PORT = int(os.getenv("HTTP_PORT", "8000"))

# store all metrics objects by their name
metrics_by_name = {}

# Updates a metric, creates it if non existent yet
def export_metric(raw_metric_name : str, metric_value : int):
    metric_name = format_to_valid_metric_name(raw_metric_name)
    
    if metric_name not in metrics_by_name:
        # Create a new metric if it doesn't exist yet
        metric = Gauge(metric_name, f"fetched by nextcloud-task-automation", registry=custom_registry)
        metrics_by_name[metric_name] = metric

    # Set the metric value
    metrics_by_name[metric_name].set(metric_value)

# Function to periodically update the metrics
def update_metrics():
    while True:
        boards = nextcloud.fetch_boards_info()
        boards_total = len(boards)
        export_metric("boards_total", boards_total)
        for board in boards:
            board_name = board["name"]
            board_lists_total = board["number_of_lists"]
            export_metric("board_%s_lists_total" % board_name, board_lists_total)
            board_cards_total = board["number_of_cards"]
            export_metric("board_%s_cards_total" % board_name, board_cards_total)
            board_lists = board["lists"]
            for list_item in board_lists:
                list_name = list_item["name"]
                list_cards_total = list_item["number_of_cards"]
                export_metric("board_%s_list_%s_cards_total" % (board_name, list_name), list_cards_total)
        print(f"Updated {len(metrics_by_name)} metrics")

        time.sleep(5)

def format_to_valid_metric_name(input_string):
    # Replace any characters that are not valid in a metric name with underscores
    sanitized_string = re.sub(r'[^a-zA-Z0-9:_]', '_', input_string)

    # Ensure the metric name starts with a letter
    if not sanitized_string[0].isalpha():
        sanitized_string = '_' + sanitized_string

    # Ensure the metric name is not empty and is not longer than 255 characters
    if not sanitized_string or len(sanitized_string) > 255:
        raise ValueError("Invalid metric name")

    return sanitized_string

if __name__ == '__main__':
    # Create a custom Prometheus registry
    custom_registry = CollectorRegistry()

    # Start the Prometheus WSGI server on desired port with the custom registry
    start_wsgi_server(HTTP_PORT, addr='0.0.0.0', registry=custom_registry)

    # Start a thread to periodically update the metrics
    update_thread = threading.Thread(target=update_metrics)
    update_thread.daemon = True
    update_thread.start()

    try:
        while True:
            # Keep the main thread alive
            time.sleep(1)
    except KeyboardInterrupt:
        pass
