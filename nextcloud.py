import os
import requests
import logging

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=LOG_LEVEL
)
logger = logging.getLogger("nextcloud")

NEXTCLOUD_USERNAME = os.getenv("NEXTCLOUD_USERNAME")
NEXTCLOUD_PASSWORD = os.getenv("NEXTCLOUD_PASSWORD")
NEXTCLOUD_HOSTNAME = "https://" + os.getenv("NEXTCLOUD_HOSTNAME")

auth = (NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD)

headers = {"Content-Type": "application/json", "OCS-APIRequest": "true"}

def _get_boards():
    """
    Fetches and returns boards from Nextcloud Deck API.
    """
    response = requests.get(
        f"{NEXTCLOUD_HOSTNAME}/index.php/apps/deck/api/v1.0/boards",
        auth=auth,
        headers=headers,
    )
    response.raise_for_status()
    return response.json()

def _get_lists(boardId):
    """
    Fetches and returns lists for a given board ID from Nextcloud Deck API.
    """
    response = requests.get(
        f"{NEXTCLOUD_HOSTNAME}/index.php/apps/deck/api/v1.0/boards/{boardId}/stacks",
        auth=auth,
        headers=headers,
    )
    response.raise_for_status()
    return response.json()

def _fetch_board_info(board):
    """
    Fetches and processes information about a single board.
    """
    board_title = board.get("title")
    board_id = board.get("id")

    if board_title is None or board_id is None:
        logger.error("Skipping board with missing title or id")
        return None

    board_lists = _get_lists(board_id)
    total_card_count, board_lists_info = _fetch_lists_info(board_lists)
    return {
        "name": board_title,
        "number_of_cards": total_card_count,
        "number_of_lists": len(board_lists),
        "lists": board_lists_info,
    }

def _fetch_lists_info(board_lists):
    """
    Fetches and processes information about lists within a board.
    """
    total_card_count = 0
    board_lists_info = []

    for board_list in board_lists:
        list_title = board_list.get("title")
        list_id = board_list.get("id")
        list_cards = board_list.get("cards", [])
        list_card_count = len(list_cards)

        board_lists_info.append({"name": list_title, "number_of_cards": list_card_count})
        total_card_count += list_card_count

    return total_card_count, board_lists_info

def fetch_boards_info():
    """
    Fetches and processes information about all boards.
    """
    boards = _get_boards()
    results_boards = []
    total_lists = 0
    total_cards = 0

    for board in boards:
        board_info = _fetch_board_info(board)
        if board_info:
            results_boards.append(board_info)

    for board_info in results_boards:
        total_lists += board_info["number_of_lists"]
        total_cards += board_info["number_of_cards"]

    logger.debug(
        "Found %i boards with %i lists and %i cards", len(boards), total_lists, total_cards
    )

    return results_boards
