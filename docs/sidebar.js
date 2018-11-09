function linkify(div,arr){
	var link = document.createElement('a');
	link.href = arr[1];
	var text = document.createTextNode(arr[0]);
	link.append(text);
	div.appendChild(link);
}

function genSidebar(){
	var side = document.createElement('div');
	side.className = 'sidebar';

	var para = document.createElement('p');
	para.className = 'sidebar-head';
	var text = document.createTextNode('Navigate');
	para.append(text);
	side.appendChild(para);

	var thisSite = 	   [['Main Page',			'index.html'],
						['Groger Scores',		'scores.html'],
						['PACE Forecast',		'pace.html'],
						['About',				'about.html']]
	var otherSites =   [['Groger Ranks',		'https://grogerranks.wordpress.com/'],
						['QB Resource Center',	'http://www.hsquizbowl.org/db/'],
						['QB Database Search',	'http://hdwhite.org/qb/stats/']]

	var para = document.createElement('p');
	para.className = 'sidebar-subhead';
	var text = document.createTextNode('This Site');
	para.append(text);
	side.appendChild(para);

	for(let link of thisSite){linkify(side,link);}

	var para = document.createElement('p');
	para.className = 'sidebar-subhead';
	var text = document.createTextNode('Other Sites');
	para.append(text);
	side.appendChild(para);

	for(let link of otherSites){linkify(side,link);}

	document.getElementsByTagName('body')[0].appendChild(side);
}