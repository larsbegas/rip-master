var links = find(/\/photo\/\d+/i);
output("LEN:" + links.length);
//for(u in links) {output('u:' + u);};
asd = find(r"/photo/\d+?");
output("asd:" + asd.length);

for (i = find(r"/photo/\d+?"); i.hasMatch; i = i.next) {
	if (i == null) {
		output("NULL");
		else output(i);
	}
}

for (link = find(/photo\/\\d*/i); link.hasMatch; link = link.next) {
	//link = links[i];
	if (link && !link.element) {
		output("PUT");
		output(link.html);
		continue;
	}
	output("<h1>" +
		links[i].element.getAttribute("href") +
		"</h1>");
}