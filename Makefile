all: index.html

force:
	bikeshed -f spec ./index.src.html

WD:
	bikeshed -f spec --md-status=WD ./index.src.html ./WD.html

index.html: index.src.html
	bikeshed -f spec ./index.src.html

publish:
	git push origin master

