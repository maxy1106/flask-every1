from App.modeles.article_models import Article


def get_article(articleId):
    """
    通过articleId获取文章信息并返回
    :param articleId:
    :return:
    """
    if not articleId:
        return None
    article = Article.query.filter(Article.id.__eq__(articleId),Article.isDelete.__eq__(False)).first()

    if not article:
        return None
    return article