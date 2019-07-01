

customElements.define('question-answers',
    class extends HTMLElement {
        constructor() {
            super();
            const innerHTML = `
                <style>
                    p {
                        color: red;
                    }
                    code {
                        color: magenta;
                        background-color: aliceblue;
                    }
                    .answers > li >b {
                        color: green;
                    }
                </style>
                <div class="question">
                    <p id="question1" class="question text">
                        what does the following code do?
                        <pre>
                            <code>
                                def a(b, c, d): pass
                            </code>
                        </pre>
                    </p>
                    <ul class="answers">
                        <li>defines a list and initializes it</li>
                        <li><b>defines a function, which does nothing</b></li>
                        <li>defines a function, which passes its parameters through</li>
                        <li>defines an empty class</li>
                    </ul>
                </div>
            `;
            let template = document.createElement('template');
            template.innerHTML = innerHTML;
            let templateContent = template.content;
            const shadowRoot = this.attachShadow(
                {mode: 'open'}
            ).appendChild(templateContent.cloneNode(true));
        }
    }
);

navigator.clipboard.readText().then(text => console.log(text))