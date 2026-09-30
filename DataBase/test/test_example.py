import pytest




def test_two_number_values_equal():
    assert 2 + 2 == 4

def test_boolean_values():
    validity = True
    assert validity is True
    assert ('John' == 'Dome') is False

def test_is_instance():
    name = "Str"
    assert isinstance(name,str)
    assert not isinstance('10',int)

def test_type_variables():
    assert type("string") is str
    assert type('num') is not int

def test_greater_less_than():
    assert 2 < 5 
    assert 12 > 5 

def test_array_values():
    arr1=[1,2,3,4,5]
    arr2=[True,True,True]
    assert 1 in arr1
    assert 7 not in arr1
    assert all(arr2) is True
    assert any(arr2) is True


class Students:
    def __init__(self , first_name : str , last_name:str , age :int , major:str):
        self.first_name = first_name
        self.last_name =  last_name
        self.age = age
        self.major = major


@pytest.fixture
def default_student():
    return Students('Far' ,'Han' , 10 , 'Cs')

def test_user_object(default_student):
    assert default_student.last_name == 'Han' , 'Last name should be Han'
    assert default_student.first_name == 'Far' , 'First name should be Far'
    assert default_student.age == 10
    assert default_student.major == 'Cs', 'Major should be cs'