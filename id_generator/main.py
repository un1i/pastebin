from fastapi import FastAPI
import generator as gen


generator = gen.Generator()
app = FastAPI()


@app.get('/')
async def default():
    result = {
        'id': generator.get_id()
    }
    return {
        'status': 'ok',
        'data': result,
        'details': None
    }


@app.on_event('startup')
async def start():
    generator.start_generate()
    print('success generate!')

