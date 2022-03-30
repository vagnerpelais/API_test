from fastapi import HTTPException, status


def id_not_found():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='id não encontrado')
