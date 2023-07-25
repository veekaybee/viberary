/**
 * <md-block> custom element
 * @author Lea Verou
 */

let marked = window.marked;
let DOMPurify = window.DOMPurify;
let Prism = window.Prism;

export const URLs = {
	marked: "https://cdn.jsdelivr.net/npm/marked/src/marked.min.js",
	DOMPurify: "https://cdn.jsdelivr.net/npm/dompurify@2.3.3/dist/purify.es.min.js"
}

// Fix indentation
function deIndent(text) {
	let indent = text.match(/^[\r\n]*([\t ]+)/);

	if (indent) {
		indent = indent[1];

		text = text.replace(RegExp("^" + indent, "gm"), "");
	}

	return text;
}

export class MarkdownElement extends HTMLElement {
	constructor() {
		super();

		this.renderer = Object.assign({}, this.constructor.renderer);

		for (let property in this.renderer) {
			this.renderer[property] = this.renderer[property].bind(this);
		}
	}

	get rendered() {
		return this.getAttribute("rendered");
	}

	get mdContent () {
		return this._mdContent;
	}

	set mdContent (html) {
		this._mdContent = html;
		this._contentFromHTML = false;

		this.render();
	}

	connectedCallback() {
		Object.defineProperty(this, "untrusted", {
			value: this.hasAttribute("untrusted"),
			enumerable: true,
			configurable: false,
			writable: false
		});

		if (this._mdContent === undefined) {
			this._contentFromHTML = true;
			this._mdContent = deIndent(this.innerHTML);
		}

		this.render();
	}

	async render () {
		if (!this.isConnected || this._mdContent === undefined) {
			return;
		}

		if (!marked) {
			marked = import(URLs.marked).then(m => m.marked);
		}

		marked = await marked;

		marked.setOptions({
			gfm: true,
			smartypants: true,
			langPrefix: "language-",
		});

		marked.use({renderer: this.renderer});

		let html = this._parse();

		if (this.untrusted) {
			let mdContent = this._mdContent;
			html = await MarkdownElement.sanitize(html);
			if (this._mdContent !== mdContent) {
				// While we were running this async call, the content changed
				// We don’t want to overwrite with old data. Abort mission!
				return;
			}
		}

		this.innerHTML = html;

		if (!Prism && URLs.Prism && this.querySelector("code")) {
			Prism = import(URLs.Prism);

			if (URLs.PrismCSS) {
				let link = document.createElement("link");
				link.rel = "stylesheet";
				link.href = URLs.PrismCSS;
				document.head.appendChild(link);
			}
		}

		if (Prism) {
			await Prism; // in case it's still loading
			Prism.highlightAllUnder(this);
		}

		if (this.src) {
			this.setAttribute("rendered", this._contentFromHTML? "fallback" : "remote");
		}
		else {
			this.setAttribute("rendered", this._contentFromHTML? "content" : "property");
		}

		// Fire event
		let event = new CustomEvent("md-render", {bubbles: true, composed: true});
		this.dispatchEvent(event);
	}

	static async sanitize(html) {
		if (!DOMPurify) {
			DOMPurify = import(URLs.DOMPurify).then(m => m.default);
		}

		DOMPurify = await DOMPurify; // in case it's still loading

		return DOMPurify.sanitize(html);
	}
};

export class MarkdownSpan extends MarkdownElement {
	constructor() {
		super();
	}

	_parse () {
		return marked.parseInline(this._mdContent);
	}

	static renderer = {
		codespan (code) {
			if (this._contentFromHTML) {
				// Inline HTML code needs to be escaped to not be parsed as HTML by the browser
				// This results in marked double-escaping it, so we need to unescape it
				code = code.replace(/&amp;(?=[lg]t;)/g, "&");
			}
			else {
				// Remote code may include characters that need to be escaped to be visible in HTML
				code = code.replace(/</g, "&lt;");
			}

			return `<code>${code}</code>`;
		}
	}
}

export class MarkdownBlock extends MarkdownElement {
	constructor() {
		super();
	}

	get src() {
		return this._src;
	}

	set src(value) {
		this.setAttribute("src", value);
	}

	get hmin() {
		return this._hmin || 1;
	}

	set hmin(value) {
		this.setAttribute("hmin", value);
	}

	get hlinks() {
		return this._hlinks ?? null;
	}

	set hlinks(value) {
		this.setAttribute("hlinks", value);
	}

	_parse () {
		return marked.parse(this._mdContent);
	}

	static renderer = Object.assign({
		heading (text, level, _raw, slugger) {
			level = Math.min(6, level + (this.hmin - 1));
			const id = slugger.slug(text);
			const hlinks = this.hlinks;

			let content;

			if (hlinks === null) {
				// No heading links
				content = text;
			}
			else {
				content = `<a href="#${id}" class="anchor">`;

				if (hlinks === "") {
					// Heading content is the link
					content += text + "</a>";
				}
				else {
					// Headings are prepended with a linked symbol
					content += hlinks + "</a>" + text;
				}
			}

			return `
				<h${level} id="${id}">
					${content}
				</h${level}>`;
		},

		code (code, language, escaped) {
			if (this._contentFromHTML) {
				// Inline HTML code needs to be escaped to not be parsed as HTML by the browser
				// This results in marked double-escaping it, so we need to unescape it
				code = code.replace(/&amp;(?=[lg]t;)/g, "&");
			}
			else {
				// Remote code may include characters that need to be escaped to be visible in HTML
				code = code.replace(/</g, "&lt;");
			}

			return `<pre class="language-${language}"><code>${code}</code></pre>`;
		}
	}, MarkdownSpan.renderer);

	static get observedAttributes() {
		return ["src", "hmin", "hlinks"];
	}

	attributeChangedCallback(name, oldValue, newValue) {
		if (oldValue === newValue) {
			return;
		}

		switch (name) {
			case "src":
				let url;
				try {
					url = new URL(newValue, location);
				}
				catch (e) {
					return;
				}

				let prevSrc = this.src;
				this._src = url;

				if (this.src !== prevSrc) {
					fetch(this.src)
					.then(response => {
						if (!response.ok) {
							throw new Error(`Failed to fetch ${this.src}: ${response.status} ${response.statusText}`);
						}

						return response.text();
					})
					.then(text => {
						this.mdContent = text;
					})
					.catch(e => {});
				}

				break;
			case "hmin":
				if (newValue > 0) {
					this._hmin = +newValue;

					this.render();
				}
				break;
			case "hlinks":
				this._hlinks = newValue;
				this.render();
		}
	}
}


customElements.define("md-block", MarkdownBlock);
customElements.define("md-span", MarkdownSpan);
