from handle.support.DB import DB as DB





result = DB().table('user').where('username','admin').first()
print(result)