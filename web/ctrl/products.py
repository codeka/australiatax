


import model.products

def getProductList(pageNo, pageSize=25):
  query = model.products.Product.all().order("updated")
  if pageNo == 0:
    it = query.run(limit=pageSize)
  else:
    cursor = ctrl.findCursor(query, "products", pageNo, pageSize)
    it = query.with_cursor(cursor)

  products = []
  for product in it:
    if len(products) > pageSize:
      break
    products.append(product)
  return products


def getProductBySlugs(companySlug, productSlug):
  companyMdl = model.products.Company.all().filter('slugs =', companySlug).fetch(1)
  if not companyMdl:
    return None
  companyMdl = companyMdl[0]

  productMdl = model.products.Product.all().filter('slugs =', productSlug).fetch(1)
  if not productMdl:
    return None
  productMdl = productMdl[0]

  return productMdl