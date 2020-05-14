from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

dros_Url = 'https://pubmed.ncbi.nlm.nih.gov/?term=drosophila+melanogaster'

# opening up connection, grabbing the page
dros_page = uReq(dros_Url)
dros_hmtl = dros_page.read()
dros_page.close()

#html paring
dros_soup = soup(dros_html, "html.parser")

#grab each articles
dros_articles = dros_soup.findAll("div", {"class":"docsum-content"})

filename = "search results.csv"
f = open(filename, "w")

headers = "article_title, article_author, article_citation, article_citation_part, publication_type, article_link\n"

f.write(headers)

for article in dros_articles:

	article_title = article.a.text.strip()
	article_author = article.div.findAll("span",{"class":"labs-docsum-authors full-authors"})[0].text
	article_citation  = article.div.findAll("span",{"class":"labs-docsum-journal-citation full-journal-citation"})[0].text
	article_citation_part = article.div.findAll("span",{"class":"citation-part"})[0].text
	pub_type = article.div.findAll("span",{"class":"publication-type spaced-citation-item citation-part"})
	#publication_type = pub_type[0].text.strip()
	article_link = article.a["href"]

	print("article_title:  " + article_title)
	print("article_authors:  " + article_author)
	print("article_citation:  " + article_citation)
	print("article_citation_part:  " + article_citation_part)
	print("publication_type:  " + publication_type)
	print("article_link:  " + article_link)

	f.write(article_title + "," + article_author.replace(",","|") + "," + article_citation + "," + article_citation_part + "," + publication_type.replace(".","") + "," + article_link + "\n")
 
f.close()	

