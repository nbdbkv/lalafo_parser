def get_category_id():
    ids = []
    with open('links') as links_file:
        lines = links_file.readlines()
        for link_id in lines:
            if link_id.__contains__("category_id"):
                start = link_id.find("category_id=") + len("category_id=")
                end = link_id.find(" ")
                ids.append(link_id[start:end])
    return ids


ids = get_category_id()
