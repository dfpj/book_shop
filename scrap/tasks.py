from celery import shared_task
from .main import main_page_scrap_and_save_db,book_scrap,image_upload_s3



@shared_task
def task_main_page_scrap():
    main_page_scrap_and_save_db()

@shared_task
def task_book_scrap():
    book_scrap()

@shared_task
def task_image_upload_s3():
    image_upload_s3()