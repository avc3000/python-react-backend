from motor.motor_asyncio import AsyncIOMotorClient
from models import Task
from bson import ObjectId

client = AsyncIOMotorClient('mongodb://localhost')
database = client.tasksDB
collection = database.tasks

async def get_one_task_id(id):
  task = await collection.find_one({'_id': ObjectId(id)})
  return task

async def get_one_task_title(title):
  task = await collection.find_one({'title': title})
  return task

async def get_all_tasks():
  tasks = []
  cursor = collection.find({})
  async for document in cursor:
    tasks.append(Task(**document))
  return tasks

async def create_task(task):
  new_task = await collection.insert_one(task)
  create_task = await collection.find_one({'_id': new_task.inserted_id})
  return create_task

async def update_task(id: str, data: Task):
  task = { k:v for k, v in data.dict().items() if v is not None }
  await collection.update_one({'_id': ObjectId(id)}, {'$set': task})
  update_task = await collection.find_one({'_id': ObjectId(id)})
  return update_task

async def delete_task(id: str):
  await collection.delete_one({'_id': ObjectId(id)})
  return True