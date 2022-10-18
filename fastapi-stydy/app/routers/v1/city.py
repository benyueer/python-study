import datetime
from typing import List, Optional, Set, Union
from fastapi import APIRouter, Body, Cookie, Depends, File, Form, Header, Path, Query, UploadFile, status, HTTPException
from app.schemas.city import CityCreateSchema
from app.database import get_db_session
from app.services.city import search, create
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from app.models.city import City

router = APIRouter(tags = ['city'])

@router.get('/')
def hello_world():
    return {'hello': 'world'}

@router.get('/city/{city}')
def result(city: str, query_string: Optional[str] = None):
    return {'city': city, 'query_string': query_string}

@router.get('/file/{file_path:path}') # 通过path转义路径
def filepath(file_path):
    return {'file_path': file_path}

# fastapi 的参数验证（数字），看Path源码
@router.get('/path/{num}')
def path_params_vaildate(
    num: int = Path(None, ge=1, le=10, description='your number', title='your numbre')
):
    return {'num': num}

# 查询参数和字符串验证
@router.get('/query')
def page_limit(page: int = 1, limit: Optional[int] = 10):  # 给了默认值就是选填参数
    if limit:
        return {'page': page, 'limit': limit}
    return {'page': page}

@router.get('/query/bool')
def query_bool(param: bool = False):
    return param


@router.get('/query/validations')
def query_params_validate(
    value: str = Query(..., min_length=3, max_length=10, regex='^a'),  # Query限制字符串验证 ...或不写default代表没有默认值，必填参数
    values: List[str] = Query(default=['v1', 'v2'], alias='alias_name')  # 列表   有default代表选填
):
    return value, values


"""请求体和字段"""
class CityInfo(BaseModel):
    name: str = Field(..., example='city name')  # 使用Field校验字段
    country: str
    country_code: Optional[str] = None
    population: int = Field(default=800, title='人口', description='renkoushu')

    class Config:   # 配置Model的信息
        schema_extra = {
            'example': {     # 示例
                'name': 'Shanghai',
                'country': 'China',
                'country_code': '#efer',
                'population': 123456
            }
        }

@router.post('/request_body/city')
def city_info(city: CityInfo):
    print(city)
    return city

"""request body + path params + query params 多参数混合"""
@router.put('/request_body/city/{name}')
def mix_city_info(
    name: str,
    city01: CityInfo,
    death: int = Query(ge=0, description='death num', default=0)
):
    if name == 'Shanghai':
        return {'Shanghai': {'a': 1}}
    return city01.dict()


"""数据格式嵌套的请求体"""
class Data(BaseModel):
    city: Optional[List[CityInfo]] = None
    date: Optional[datetime.date] = None

@router.put('/request_body/nested')
def nested_models(data: Data):
    return data


"""cookie 和 header 参数"""
@router.get('/cookie')
def cookie(cookie_id: Optional[str] = Cookie(None)):
    return cookie_id

@router.get('/header')
def header(
    user_agent: Optional[str] = Header(None, convert_underscores=True),
    x_token: List[str] = Header(None)
):
    """
    有些代理和服务器不允许请求头使用下划线，convert_underscores属性转下划线
    """
    return {'user_agent': user_agent, 'x_token': x_token}


"""Response Model 响应模型"""
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserOut(BaseModel):
    username: str
    email: EmailStr
    one: str = 'dasdasd'

users = {
    'user01': {'username': 'name1', 'password': '1231312', 'email': 'qwewqe@rewrew.cdd'},
    'user02': {'username': 'name2', 'password': '1231312', 'email': 'qwewqe@rewrew.cdd', 'msg': 'adasdasd'}
}

@router.post(
    '/response_model',
    response_model=UserOut,
    response_model_exclude_unset=True
)
async def response_model(user: UserIn):
    """
    response_model_exclude_unset 表示默认值不包含在响应中, 如设置为True时不会返回 one 字段
    """
    print(user.username)
    return users['user02']

@router.post(
    '/response_model/attr',
    response_model=Union[UserIn, UserOut],  # Union 合并类型，包括所有类型的所有字段
    # response_model=List[UserOut]   或使用List，表示列表中的任意一个类型都可以
    response_model_include=set(['username']),  # 表示包含哪些字段  
    response_model_exclude=set(['password'])  # type: ignore # 表示排除字段  
)
def response_model_attr(user: UserIn):
    # del user.password   # 如果不想返回password，del掉
    return user


"""响应状态码"""
@router.get(
    '/status_code',
    # status_code=200
    status_code=status.HTTP_200_OK
)
def status_code():
    return {'msg': 'hello world'}


"""Form Data表单数据处理"""
@router.post('/login')
def login(user: str = Form(), password: str = Form()):
    """Form Class need python-multipart, Form类的元数据校验类似Query、Body等"""
    return {'username': user, 'password': password}


"""文件上传"""
@router.post('/file')
async def file_(path: str = Body(), file: List[bytes] = File()):
    """
    上传多个文件使用List
    这样文件会在内存中，只能上传小文件
    """
    return {'file_size': len(file[0])}

@router.post('/upload_files')
async def upload_files(files: List[UploadFile] = File()):
    """
    upload_file类上传文件时，当内存使用达到阈值时，会将文件写到硬盘
    适合大文件
    可以获取文件完整的元数据：文件名、创建时间等
    有文件对象的异步接口
    上传的文件时Python文件对象，可以使用write、read等方法
    """
    filesContents = []
    filenames = []
    for file in files:
        filenames.append(file.filename)
        contents = len(await file.read())
        print(contents)
        filesContents.append(contents)
    return filesContents, filenames


"""Path Operation Config 路径操作配置"""
@router.get(
    '/path_operation_config',
    response_model=UserOut,
    tags=['Path', 'Operation', 'Config'],
    summary='this is summary',
    description='this is description',
    response_description='this is response description',
    status_code=status.HTTP_200_OK
)
async def path_operation_config():
    return 123


"""Handling Errors 错误处理"""
@router.get('/http_exception')
async def http_exception(city: str):
    if city != 'Beijing':
        raise HTTPException(status_code=404)
    return {'city': city}

@router.get('/http_exception_overwrite')
async def http_exception_overwrite(city: str):
    if city != 'Beijing':
        raise HTTPException(status_code=404)  # 被重写为500
    return {'city': city}



"""Dependencies 依赖创建、声明和导入"""
async def common_parameters(q: Optional[str] = None, page: int = 1, limit: int = 10):
    return {'q': q, 'page': page, 'limit': limit}

@router.get('/dependency_1')
async def dependency_1(commons: dict = Depends(common_parameters)):
    return commons


"""Classes as Dependencies 类作为依赖项"""
fake_items = [
    {'name': 'Foo'},
    {'name': 'Bar'},
    {'name': 'Baz'},
]

class CommonQueryParams:
    def __init__(
        self,
        q: Optional[str] = None,
        page: int = 1,
        limit: int = 10
    ):
        self.q = q
        self.page = page
        self.limit = limit

@router.get('/classes_as_dependencies')
async def classes_as_dependencies(
    commons: CommonQueryParams = Depends(CommonQueryParams),
    commons1: CommonQueryParams = Depends(),
    commons2 = Depends(CommonQueryParams),
):
    response = {}
    if commons.q:
        response['q']= commons.q
    items = fake_items[commons.page: commons.page + commons.limit]
    return commons, commons1, commons2, items
    
"""Sun Dependencies 子依赖"""
def query(q: Optional[str] = None):
    return q

def sub_query(q: str = Depends(query), last_query: Optional[str] = 'None'):
    if not q:
        return last_query
    return q

@router.get('/sub_dependencies')
async def sub_dependency(finally_query: str = Depends(sub_query, use_cache=True)):
    """
    使用缓存
    """
    return finally_query


"""在路径操作导入依赖"""
async def verfiy_token(x_token: str = Header()):
    """没有返回值的子依赖"""
    if x_token != 'is token':
        raise HTTPException(status_code=404)
    return x_token

async def verfiy_key(x_key: str = Header()):
    """没有返回值的子依赖"""
    if x_key != 'is key':
        raise HTTPException(status_code=567)
    return x_key

@router.get('/dependencies_in_path_operation', dependencies=[Depends(verfiy_key), Depends(verfiy_token)])
async def dependencies_in_path_operation():
    return [{'name': 'adsad'}]



"""Global 全局依赖"""
# app = APIRouter(dependencies=[Depends(verfiy_token)])


"""Dependencies with yield 带yield的依赖"""


"""OAuth2 密码模式和 FastAPI 的 OAuth2PasswordBearer"""
"""不会创建URL路径操作 只是指明客户端用来请求Token的URL地址"""
oathh2_schema = OAuth2PasswordBearer(tokenUrl='/v1/token')

@router.get('/oauth2_password_bearer')
async def oauth2_password_bearer(token: str = Depends(oathh2_schema)):
    return {"token": token}


"""基于 Password 和 Bearer token 的 OAtuh2 认证"""
fake_users_db = {
    "hello": {
        "name": 'hello',
        'password': 'password1',
    }
}

class User(BaseModel):
    name: str
    password: str

def get_current_user(token: User = Depends(oathh2_schema)):
    print(token)
    return token

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return User(**user_dict)
    
@router.post('/token')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):

    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    user = get_user(fake_users_db, form_data.username)
    if not user or not user.password == form_data.password:
        raise 
    return {'access_token': user.name, 'token_type': 'bearer'}

@router.get('/user/me')
def read_user_me(current_user: User = Depends(get_current_user)):
    """获取当前用户"""
    return current_user

@router.get('/citys')
def citys(offset: int, limit: int, db_session=Depends(get_db_session)):
    return search(offset, limit, '', db_session)

@router.post('/city')
def create_city(city: CityCreateSchema, db_session=Depends(get_db_session)):
    return create(city, db_session)