from prometheus_client import start_wsgi_server, CollectorRegistry, Gauge
import threading
import time
import random
import re
from nextcloud import fetchBoardsInfo

# Function to periodically update the metric
def update_metrics():
    while True:
        # Simulate fetching new data (replace this with your actual data source)
        new_data = random.randint(1, 100)
        metric.set(new_data)

        # Print the updated data (for demonstration purposes)
        print(f"Updated metric value: {new_data}")

        time.sleep(1)

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

# Example usage:
input_string = "  My Metric Name 123!@#"
valid_metric_name = format_to_valid_metric_name(input_string)
print(valid_metric_name)

if __name__ == '__main__':
    # Create a custom Prometheus registry
    custom_registry = CollectorRegistry()

    # Define your custom metric and register it with the custom registry
    metric = Gauge(valid_metric_name, 'description_XY', registry=custom_registry)

    # Start the Prometheus WSGI server on port 8000 with the custom registry
    start_wsgi_server(8000, addr='0.0.0.0', registry=custom_registry)

    # Start a thread to periodically update the metric
    update_thread = threading.Thread(target=update_metrics)
    update_thread.daemon = True
    update_thread.start()

    try:
        while True:
            # Keep the main thread alive
            time.sleep(1)
    except KeyboardInterrupt:
        pass
