import pytchat
chat = pytchat.create(video_id="9B_VJRMgyBA")
while chat.is_alive():
    for c in chat.get().sync_items():
        print(f"{c.datetime} [{c.author.name}]- {c.message}")