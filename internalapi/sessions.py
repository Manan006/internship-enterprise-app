from internalapi.cache import cache
from internalapi.methods import methods
from internalapi.db import Cursor
from internalapi.users import user
from internalapi.response import Response
class session:
    def get(id):
        return cache.get("sessions",id)
    def set(employ:user.userObject):
        while True:
            session_id=methods.generateRandom(32)
            prepare=f"SELECT EXISTS(SELECT `key` FROM `cache` WHERE `namespace`='sessions' AND `key`='{session_id}' LIMIT 1)"
            Cursor.execute(prepare)
            if Cursor.fetchall()[0][0]!=True:
                break
        cache.set("sessions",session_id,employ.id)
        sessions=employ.sessions
        sessions.append(session_id)
        employ.edit(attr="sessions",value=sessions)
        return Response(100,session_id)
    def remove(id):
        return cache.removes("sessions",id)
