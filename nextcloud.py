import datetime
import os
import requests
import re
import yaml
from pprint import pprint
import logging

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.ERROR
)
logger = logging.getLogger("log")
logger.setLevel(LOG_LEVEL)

NEXTCLOUD_USERNAME = os.getenv("NEXTCLOUD_USERNAME")
NEXTCLOUD_PASSWORD = os.getenv("NEXTCLOUD_PASSWORD")
NEXTCLOUD_HOSTNAME = "https://" + os.getenv("NEXTCLOUD_HOSTNAME")

auth = (NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD)

headers = {"Content-Type": "application/json", "OCS-APIRequest": "true"}

def getBoards():
    logger.debug("getBoards()")
    response = requests.get(
            f"{NEXTCLOUD_HOSTNAME}/index.php/apps/deck/api/v1.0/boards",
            auth = auth,
            headers=headers)
    response.raise_for_status()
    return response.json()

def getLists(boardId):
    logger.debug("getLists()")
    response = requests.get(
            f"{NEXTCLOUD_HOSTNAME}/index.php/apps/deck/api/v1.0/boards/{boardId}/stacks",
            auth=auth,
            headers=headers)
    response.raise_for_status()
    return response.json()

def fetchBoardsInfo():
    # fetch boards
    boards = getBoards()
    results_boards = []
    board_id = None
    automation_board = None
    total_boards = len(boards)
    total_lists = 0
    total_cards = 0
    for board in boards:
        total_board_cards = 0
        board_title = board.get("title")
        if board_title == None:
            logger.error("board has no title")
        board_id = board.get("id")
        if board_id == None:
            logger.error("board has no id")
        logger.debug("- %s", board_title)
        board_lists = getLists(board_id)
        total_lists += len(board_lists)
        new_board_lists_item = []
        for board_list in board_lists:
            list_title = board_list.get("title")
            if list_title == None:
                logger.error("list has no title")
            list_id = board_list.get("id")
            if list_id == None:
                logger.error("list has no id")
            list_cards = board_list.get("cards")
            if list_cards == None:
                logger.debug("list is empty")
                list_cards = []
            new_board_lists_item += {"name": list_title, "number_of_cards": len(list_cards)}
            logger.debug("List '%s' has %i cards", list_title, len(list_cards))
            total_board_cards += len(list_cards)
            total_cards += len(list_cards)

        results_boards_item = {"name": board_title, "number_of_cards": total_board_cards, "number_of_lists": len(board_lists), "lists": new_board_lists_item}
        results_boards.append(results_boards_item)
        logger.debug("Board '%s' has %i lists and %i cards in total", board_title, len(board_lists), total_board_cards)
    logger.info("Found %i boards with %i lists and %i cards", len(boards), total_lists, total_cards)

    return results_boards
