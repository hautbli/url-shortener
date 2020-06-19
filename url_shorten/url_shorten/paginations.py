from rest_framework.pagination import CursorPagination


class listpagination(CursorPagination):
    # 오버라이딩 안하면 디폴트 created로 돼서 에러가 뜬다.-> 찾기 매우어려웠다..
    ordering =  '-id'