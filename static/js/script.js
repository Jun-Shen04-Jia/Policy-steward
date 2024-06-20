function notify(num = 3, properties) {
	const defaultProperties = {
		element: document.querySelector(".bell-icon"),
		badgeColor: "steelblue",
		badgeTextColor: "#fff",
		ballColor: "#000",
		bellColor: "#000",
		outlineWidth: 10,
		ringSpeed: 400,
		title: `${num} notifications!`,
		upperLimit: 9
	};
	const n = Object.assign(defaultProperties, properties);
	let notification = n.element;
	notification.title = `${num} notifications!`;
	// remove any old svgs
	while (notification.firstChild) {
		notification.removeChild(notification.firstChild);
	}
	let notificationNum = "";
	let numOffset = "0 0";
	if (num > n.upperLimit) num = n.upperLimit;
	for (let i = 1; i <= num; i++) {
		let plus = "";
		let dblOff = 0;
		if (i == n.upperLimit || i > 9) dblOff = 6;
		if (i == n.upperLimit) plus = "+";
		notificationNum += `<text x="${(100 * i) - dblOff}" y="0" font-size="20" fill="${n.badgeTextColor}" font-weight="600" font-family="monospace">${i}${plus}</text>`;
		numOffset += `;${-100 * i} 0`;
	}
	let svg = `<svg class="bell-icon" viewBox="0 0 100 100" height="100%" width="100%"><defs>
	<path id="bellBody${num}" d="M 44 8 A 1 1 0 0 1 56 8 V 12 Q 80 17 80 41 Q 80 61 90 69 C 94 72 92 80 86 80 H 14 C 8 80 6 72 10 69 Q 20 61 20 41 Q 20 17 44 12 Z" fill="${n.bellColor}"><animateTransform attributeName="transform" attributeType="XML" type="rotate" values="0 50 45; -12 50 45; 0 50 45; 12 50 45; 0 50 45" dur="${n.ringSpeed}ms" begin="0s" repeatCount="${num}" keyTimes="0;0.4;0.5;0.6;1" keySplines="0.67 0.01 0.39 0.98; 0.67 0.01 0.39 0.98; 0.67 0.01 0.39 0.98; 0.67 0.01 0.39 0.98" calcMode="spline" /></path><circle id="badge${num}" cx="83" cy="27" r="15" fill="${n.badgeColor}"><animate attributeName="r" values="15;17;15" dur="${n.ringSpeed}ms" begin="0s" repeatCount="${num}" /></circle><mask id="mBell${num}"><rect x="0" y="0" width="100" height="100" fill="#fff" /><use href="#bellBody${num}" fill="#000" stroke="#000" stroke-width="${n.outlineWidth}"/></mask><mask id="m${num}"><rect x="0" y="0" width="100" height="100" fill="#fff" /><use href="#badge${num}" fill="#fff" stroke="#000" stroke-width="${n.outlineWidth}" /></mask><mask id="mm${num}"><circle cx="83" cy="27" r="15" fill="#fff" /></mask></defs><g mask="url(#m${num})"><use href="#bellBody${num}" /><circle class="bellGong" cx="50" cy="85" r="11" fill="${n.ballColor}" mask="url(#mBell${num})"><animate attributeName="cx" values="50; 40; 50; 60; 50" dur="${n.ringSpeed}ms" begin="0s" repeatCount="${num}" keyTimes="0;0.4;0.5;0.6;1" keySplines="0.67 0.01 0.39 0.98; 0.67 0.01 0.39 0.98; 0.67 0.01 0.39 0.98; 0.67 0.01 0.39 0.98" calcMode="spline" /></circle></g><use href="#badge${num}" /><g mask="url(#mm${num})"><g transform="translate(77 34)"><g>${notificationNum}<text x="0" y="0" font-size="20" fill="#fff" font-weight="600" font-family="monospace">0</text><animateTransform attributeName="transform" type="translate" values="${numOffset}" dur="${num * n.ringSpeed}ms" begin="0s" calcMode="discrete" fill="freeze" /></g></g></g></svg>`;
	const wrapper = document.createElement("div");
	wrapper.innerHTML = svg;
	const fc = wrapper.firstChild;
	notification.appendChild(fc);
}

// use the notify function to populate a container of fixed height and width with a bell
notify(2);

// 使用 AJAX 请求获取数据
$.getJSON('/get_data', function (data) {
	console.log('Data from Flask:', data);

	// 如果 type 是 'notify' 并且 value 是 2，就调用 notify 函数
	if (data.type === 'notify' && data.value === 2) {
		notify(data.value);
	}
});