from internalapi.cache import cache
from internalapi.methods import methods
from internalapi.db import Cursor
from internalapi.users import user
from internalapi.response import Response
class session:
    def get(id):
        id=cache.get("sessions",id)
        if not id.success:
            return id
        return user.fetch(id.content)
    def set(employ:user.userObject):
        while True:
            session_id=methods.generateRandom(32)
            prepare=f"SELECT EXISTS(SELECT `key` FROM `cache` WHERE `namespace`='sessions' AND `key`=%s LIMIT 1)"
            Cursor.execute(prepare,(session_id,))
            if Cursor.fetchall()[0][0]!=True:
                break
        cache.set("sessions",session_id,employ.id)
        sessions=employ.sessions
        sessions.append(session_id)
        employ.edit(attr="sessions",value=sessions)
        return Response(100,session_id)
    def remove(id):
        employ=session.get(id)
        if not employ.success:
            return Response(202)
        cache.remove("sessions",id)
        employ=employ.content
        sessions=employ.sessions
        sessions.remove(session_id)
        employ.edit(attr="sessions",value=sessions)
