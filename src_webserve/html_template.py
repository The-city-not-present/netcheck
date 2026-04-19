
import re
import html





TEMPLATE_HTML_CSS_NORMALIZECSS = """
article,aside,details,figcaption,figure,footer,header,hgroup,nav,section,summary{display:block;}audio,canvas,video{display:inline-block;*display:inline;*zoom:1;}audio:not([controls]) {display:none;height:0;}[hidden]{display:none;}html{font-size:100%;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;}html,button,input,select,textarea{font-family:sans-serif;}body{margin:0;}a:focus{outline:thin dotted;}a:active,a:hover{outline:0;}h1{font-size:2em;margin:0.67em 0;}h2{font-size:1.5em;margin:0.83em 0;}h3{font-size:1.17em;margin:1em 0;}h4{font-size:1em;margin:1.33em 0;}h5{font-size:0.83em;margin:1.67em 0;}h6{font-size:0.75em;margin:2.33em 0;}abbr[title]{border-bottom:1px dotted;}b,strong{font-weight:bold;}blockquote{margin:1em 40px;}dfn{font-style:italic;}mark{background:#ff0;color:#000;}p,pre{margin:1em 0;}code,kbd,pre,samp{font-family:monospace,serif;_font-family:'courier new',monospace;font-size:1em;}pre{white-space:pre;white-space:pre-wrap;word-wrap:break-word;}q{quotes:none;}q:before,q:after{content:'';content:none;}small{font-size:75%;}sub,sup{font-size:75%;line-height:0;position:relative;vertical-align:baseline;}sup{top:-0.5em;}sub{bottom:-0.25em;}dl,menu,ol,ul{margin:1em 0;}dd{margin:0 0 0 40px;}menu,ol,ul{padding:0 0 0 40px;}nav ul,nav ol{list-style:none;list-style-image:none;}img{border:0;-ms-interpolation-mode:bicubic;}svg:not(:root) {overflow:hidden;}figure{margin:0;}form{margin:0;}fieldset{border:1px solid #c0c0c0;margin:0 2px;padding:0.35em 0.625em 0.75em;}legend{border:0;padding:0;white-space:normal;*margin-left:-7px;}button,input,select,textarea{font-size:100%;margin:0;vertical-align:baseline;*vertical-align:middle;}button,input{line-height:normal;}button,html input[type="button"],input[type="reset"],input[type="submit"]{-webkit-appearance:button;cursor:pointer;*overflow:visible;}button[disabled],input[disabled]{cursor:default;}input[type="checkbox"],input[type="radio"]{box-sizing:border-box;padding:0;*height:13px;*width:13px;}input[type="search"]{-webkit-appearance:textfield;-moz-box-sizing:content-box;-webkit-box-sizing:content-box;box-sizing:content-box;}input[type="search"]::-webkit-search-cancel-button,input[type="search"]::-webkit-search-decoration{-webkit-appearance:none;}button::-moz-focus-inner,input::-moz-focus-inner{border:0;padding:0;}textarea{overflow:auto;vertical-align:top;}table{border-collapse:collapse;border-spacing:0;}
    """

TEMPLATE_HTML_STYLES = """
    body {
        font-size: 14px;
        Font-family: "Helvetica";
    }
    * {
        box-sizing: border-box;
    }
    .clearfix:after {
       content: " "; /* Older browser do not support empty content */
       visibility: hidden;
       display: block;
       height: 0;
       clear: both;
    }
   .error {
        color: #cc0000;
        font-weight: 500;
    }
   .container {
        margin: 0 15px 0;
    }
    @media all and (min-width: 1300px) {
        .container {
            margin: 0 auto 0;
            width: 1200px;
        }
    }
    @media all and (min-width: 1650px) {
        .container {
            margin: 0 auto 0;
            width: 1500px;
        }
    }
    @media all and (min-width: 1800px) {
        .container {
            margin: 0 auto 0;
            width: 1700px;
        }
    }
    h1 {
        font-weight: 700;
        font-size: 32px;
        color: #333;
        margin: 0;
        padding: 0px 0 30px;
    }
    h2 {
        font-weight: 700;
        font-size: 21px;
        color: #222;
        margin: 0;
        padding: 22.5px 0 7.5px;
    }
    h3 {
        font-weight: 700;
        font-size: 17px;
        color: #111;
        margin: 0;
        padding: 22.5px 0 7.5px;
    }
    .header {
        padding: 15px 0 15px;
        border-bottom: 1px solid #eee;
    }
    .footer {
        padding: 15px 0 15px;
        border-top: 1px solid #eee;
    }
    .main {
        padding: 15px 0 15px;
    }
    .wrapper {
        width: 100%; max-width: 100%; overflow-x: auto;
    }
    .mdmreport-banner {
        display: block; position: relative; padding: 1em; margin: 0 0 1em; border: #ddd solid 1px;
    }
    .mdmreport-banners-wrapper-noborders .mdmreport-banner {
        padding: 0;
        border: none;
    }
    .mdmreport-banners-wrapper-noborders .mdmreport-banner h3 {
        margin-top: 0;
    }
    .mdmreport-contentcell-fullwidth {
        width: 100%;
        min-width: 100%;
    }
    .mdmreport-table-dummy .mdmreport-record .mdmreport-contentcell {
        padding: 7.5px 7.5px 7.5px 15px;
    }
"""

TEMPLATE_HTML_STYLES_TABLE = r"""
.mdmreport-section-wrapper {
    /* font-size: 12px; */
    font-size: 13px;
}
.mdmreport-table-wrapper {
    overflow-x: scroll;
}
.mdmreport-table, mdmreport-table tbody, .mdmreport-table thead, .mdmreport-table tr, .mdmreport-table td {
    margin: 0;
    padding: 0;
    line-height: 16px;
    border-collapse: collapse; border-spacing: 1px;
    border: 1px #ddd solid;
}

.mdmreport-table { width: 100%; min-width: 100%; max-width: 100%; display: block; }

.mdmreport-section-wrapper .mdmreport-banner {
    color: #555;
}
.mdmreport-section-wrapper .mdmreport-banner p {
    margin: 0.1em 0;
}

.mdmreport-table tr td {
    vertical-align: top;
}

.mdmreport-contentcell, .mdmreport-contentcell pre {
    font-family: monospace, monospace;
    font-size: 100%;
    margin: 0;
}
.mdmreport-contentcell pre {
    white-space: pre;
    overflow-x: scroll;
}
.mdmreport-contentcell p {
    margin: 0;
}

.mdmreportpage-type-MDDDiff .mdmreport-table td.mdmreport-colindex-0 {
    padding: 0.25em;
    /* font-size: 89%; */
    width: 5em; min-width: 5em; max-width: 5em;
    overflow-x: hidden;
    white-space: nowrap;
}
.mdmreport-table .mdmreport-record {
    background: #fff;
    transition: all 200ms ease;
}

.mdmreport-table .mdmreport-record:hover {
    background: #efefef;
}

/* all regular cells */ .mdmreport-table .mdmreport-record td {
    padding: 0.15em 0.35em;
    /* max-width: 15em; */
    /* max-width: 100%; */
    min-width: 60px;
    overflow: hidden;
    overflow-wrap: anywhere;
}
.mdmreport-table td.mdmreport-col-flagdiff {
    max-width: 130px;
}.mdmreport-table td.mdmreport-col-name {
    max-width: 300px;
}
.mdmreport-table td.mdmreport-col-col_x95_axis_x40_side_x41_ {
    /* for excel */
    max-width: 200px;
    min-width: 200px;
    width: 200px;
}
/* first row */ .mdmreport-table .mdmreport-record:first-child td {
    font-weight: 600;
    padding-top: 0.85em;
    padding-bottom: 0.85em;
    font-size: 100%;
    border: 0.5px solid #666666;
    background: #e1e1e1;
    border-bottom: 4px solid #217346;
}

.mdmreport-table.mdmreport-table-noborder .mdmreport-record td {
    border-width: 0;
    padding: 3px 8px 3px 0;
}
.mdmreport-table.mdmreport-table-noborder tr.mdmreport-record {
    border-width: 0;
    padding: 0;
}



.mdmreport-table .mdmreport-record {
    position: relative;
}
.mdmreport-table .mdmreport-record.mdmdiff-added {
    background: #c8f0da;
}
/* .mdmreport-table .mdmreport-record.mdmdiff-added td { */
/*     padding-top: 1.2em; */
/* } */
/* .mdmreport-table .mdmreport-record.mdmdiff-added td:first-child:before { */
/*     content: ""added""; */
/*     display: block; */
/*     position: absolute; */
/*     padding-right: 0.5em; */
/*     top: 0; */
/*     padding-top: 0; */
/*     color: #090; */
/*     z-index: 999; */
/*     font-weight: 700; */
/*     font-size: 70%; */
/* } */
.mdmreport-table .mdmreport-record.mdmdiff-removed {
    background: #ffcbbd;
}
/* .mdmreport-table .mdmreport-record.mdmdiff-removed td { */
/*     padding-top: 1.2em; */
/* } */
/* .mdmreport-table .mdmreport-record.mdmdiff-removed td:first-child:before { */
/*     content: ""removed""; */
/*     display: block; */
/*     position: absolute; */
/*     padding-right: 0.5em; */
/*     top: 0; */
/*     padding-top: 0; */
/*     color: #b00; */
/*     z-index: 999; */
/*     font-weight: 700; */
/*     font-size: 70%; */
/* } */
.mdmreport-table .mdmreport-record.mdmdiff-ghost {
    background: #fff5da;
    color: #444444;
}
.mdmreport-table tr.mdmreport-record.mdmdiff-ghost, .mdmreport-table tr.mdmreport-record.mdmdiff-movedfrom {
    background: repeating-linear-gradient(45deg, #e5e5e5, #e5e5e5 20px, #eaeaea 21px, #eaeaea 40px);
}
.mdmreport-table .mdmreport-record.mdmdiff-diff {
    background: #ffe49c;
}
.mdmreport-table .mdmreport-record.mdmdiff-diff.mdmdiff-specialtype-routing, .mdmreport-table .mdmreport-record.mdmdiff-diff.mdmdiff-specialtype-routing:hover {
    background: #f2f2f2;
}
.mdmreport-prop-fieldvalue {
    color: #600060;
}

td.mdmreport-contentcell label {
    display: block;
    font-weight: 400;
    color: #666;
    font-size: 90%;
    padding: 0.25em 0 0.25em 1em;
    position: relative;
}

.mdmdiff-inlineoverlay-added { background: #6bc795; }
.mdmdiff-inlineoverlay-removed { background: #f59278; }
.mdmdiff-inlineoverlay-diff { background: #edbf45; }

.mdmreport-format-multiline {
    /* white-space: nowrap; */
    white-space: pre;
    white-space: pre;
}
.mdmreport-format-multiline br {
    display: none;
}
.mdmreport-format-hidden, .mdmreport-table .mdmreport-format-hidden {
    display: none;
}
.mdmreport-sronly {
    visibility: hidden;
    display: block;
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0,0,0,0);
    border: 0;
}
.mdmreport-label-pseudo[data-added] {
    position: relative;
}
.mdmreport-label-pseudo[data-added]:after, .mdmreport-label-pseudo[data-added]::after {
    content: attr(data-added);
    white-space: pre;
    display: block;
    font-weight: 400;
    color: #666;
    font-size: 90%;
    padding: 0.25em 0 0.25em 1em;
    position: relative;
}

/* controls */

.mdmreport-controls fieldset, fieldset.mdmreport-controls, .mdmreport-controls form, form.mdmreport-controls { display: block; border: none; margin: 0; padding: 0; }
.mdmreport-controls legend, .mdmreport-controls label {
    display: inline-block;
    line-height: 1.3em;
    padding: 0 0.65em 0 0.65em;
    min-height: 1.7em;
}
.mdmreport-controls label {
    border: 1px solid transparent;
    transition: all 350ms ease;
}
.mdmreport-controls label:hover {
    border: 1px solid #ddd;
}
.mdmreport-controls label input[type="checkbox"] {
    display: inline-block;
    width: 0;
    margin-left: 1.35em;
    position: relative;
}
.mdmreport-controls label input[type="checkbox"]:before {
    content: " ";
    display: block;
    text-align: center;
    position: absolute;
    width: 1em;
    height: 1em;
    background: #fff;
    border: 1px solid #ddd;
    right: 100%;
    transform: translateX(-0.35em);
    line-height: .8em;
    padding: 0.1em 0 0.1em;
}
.mdmreport-controls label input[type="checkbox"]:checked:before {
    content: "\002A09";
}
.mdmreport-controls.mdmreport-controls-checkboxfulltext label input[type="checkbox"], .mdmreport-controls .mdmreport-controls-checkboxfulltext label input[type="checkbox"], .mdmreport-controls label.mdmreport-controls-checkboxfulltext input[type="checkbox"] {
    margin-left: 4.85em;
    font-family: monospace;
}
.mdmreport-controls.mdmreport-controls-checkboxfulltext label input[type="checkbox"]:before, .mdmreport-controls .mdmreport-controls-checkboxfulltext label input[type="checkbox"]:before, .mdmreport-controls label.mdmreport-controls-checkboxfulltext input[type="checkbox"]:before {
    content: "\0000A0\0000A0Hide";
    width: 4.5em;
    font-family: monospace;
    text-align: center;
    color: #888;
}
.mdmreport-controls.mdmreport-controls-checkboxfulltext label input[type="checkbox"]:checked:before, .mdmreport-controls .mdmreport-controls-checkboxfulltext label input[type="checkbox"]:checked:before, .mdmreport-controls label.mdmreport-controls-checkboxfulltext input[type="checkbox"]:checked:before {
    content: "\002A09\0000A0Show";
}
.mdmreport-controls-group input.mdmreport-controls[type="text"], .mdmreport-controls .mdmreport-controls-group input[type="text"] {
    display: block;
    line-height: 1em;
    padding: 0.35em;
    min-height: 1.3em;
    width: 100%;
    border: 1px solid #dddddd;
    border-radius: 0.18em;
}

.mdmreport-controls[disabled], .mdmreport-controls.disabled {
    position: relative;
}
.mdmreport-controls[disabled]:before, .mdmreport-controls.disabled:before {
    content: " ";
    display: block;
    position: absolute;
    left: 0; top: 0; right: 0; bottom: 0;
    background: rgba(224,224,224,0.55);
}
</style>

    """

TEMPLATE_HTML_SCRIPTS = r"""
<script>
(function() {
    /* === beautify dates js === */
    function beautifyDates() {
        let errorBannerEl = null;
        try {
            errorBannerEl = document.querySelector('#error_banner');
            if( !errorBannerEl ) throw new Error('no error banner, stop execution of js scripts');
        } catch(e) {
            throw e;
            return;
        }
        try {
            const elements = document.querySelectorAll('[data-role="date"]');
            Array.prototype.forEach.call(elements,function(el) {
                const content = el.innerText||el.textContent;
                const dt = /[1-9]/.test(content) ? new Date(content) : undefined;
                // const result = dt ? `original: ${content}, converted: ${dt}` : content; // for debugging
                const result = dt ? `${dt}` : content;
                el.innerText = result;
            });
            document.removeEventListener('DOMContentLoaded',beautifyDates);
        } catch(e) {
            try {
                function escapeHtml(s) {
                    const dummy = document.createElement('div');
                    dummy.innerText = s.replace(/\n/ig,'\\n');
                    return dummy.innerHTML;
                }
                errorBannerEl.innerHTML = errorBannerEl.innerHTML + escapeHtml(`Error: ${e}`)+'<br />';
            } catch(ee) {};
            try {
                document.removeEventListener('DOMContentLoaded',beautifyDates);
            } catch(ee) {}
            throw e;
        }
    }
    window.addEventListener('DOMContentLoaded',beautifyDates);
})()
</script>
<script>
    /* === align col widths js === */
(function() {
    function alignColWidths() {
        /* if( document.documentElement.innerHTML.length > 10000000 )
            return; */
        let errorBannerEl = null;
        try {
            errorBannerEl = document.querySelector('#error_banner');
            if( !errorBannerEl ) throw new Error('no error banner, stop execution of js scripts');
        } catch(e) {
            throw e;
            return;
        }
        try {
            /* const tables_all = document.querySelectorAll('.mdmreport-table'); */
            const cssSheet = new CSSStyleSheet();
            document.adoptedStyleSheets = [...document.adoptedStyleSheets,cssSheet];
            function process() {
                try {
                    const widthDefault = 300;
                    const tables_all = document.querySelectorAll('.mdmreport-table');
                    // first, clear out previous formatting
                    Array.prototype.forEach.call(tables_all,function(tableEl) {
                        tableEl.classList.remove('mdmreport-table-formatting-fixeddimensions');
                    });
                    cssSheet.replaceSync('');
                    (function() {
                        const widthRaw = widthDefault;
                        const widthVal = `${widthRaw}px`;
                        const cssSyntax = `.mdmreport-table td { max-width: ${widthVal}; }`
                        cssSheet.replaceSync(cssSyntax);
                    })();
                    /* stop if data is too big */
                    if( Array.from(document.querySelectorAll('.mdmreport-table td')).length>500*16*26 )
                        return;
                    // now find new width values
                    const colWidthsData = (function(){
                        const result = [];
                        Array.prototype.forEach.call(tables_all,function(tableEl,tableIndex) {
                            const rowElements = tableEl.querySelectorAll('tr.mdmreport-record');
                            if( rowElements.length>0 ) {
                                colElements = rowElements[0].querySelectorAll('tr.mdmreport-record>td');
                                Array.prototype.forEach.call(colElements,function(colEl,colIndex) {
                                    if(!result[colIndex]) result[colIndex] = [];
                                    result[colIndex][tableIndex] = colEl.getBoundingClientRect().width;
                                });
                            }
                        });
                        return result;
                    })();
                    const colMaxIndex = colWidthsData.length-1;
                    const colParentWidth = (function(){
                        var result = 0;
                        Array.prototype.forEach.call(tables_all,function(tableEl,tableIndex) {
                            if(!(result>0)) {
                                if(!!tableEl.parentElement) {
                                    result = tableEl.parentElement.getBoundingClientRect().width;
                                }
                            }
                        });
                        return result;
                    })();
                    const numColsCounted = (function(){
                        const isValValid = val => isFinite(val) && (val>0);
                        var result = [];
                        for(let colIndex=0;colIndex<=colMaxIndex;++colIndex) {
                            Array.prototype.forEach.call(tables_all,function(tableEl,tableIndex) {
                                const val = colWidthsData[colIndex][tableIndex];
                                if(isValValid(val)) {
                                    result[colIndex] = 1;
                                }
                            });
                        }
                        return result.reduce((acc,e)=>acc+(e>0?1:0),0);
                    })();
                    const colMinWidth = 60;
                    const colMaxAllowedWidth = (function(){
                        var result = document.querySelector('body').getBoundingClientRect().width;
                        if( numColsCounted==1 ) {
                            result = colParentWidth;
                        } else {
                            const resultVerA = colParentWidth - colMinWidth * 1.19 >= colMinWidth ? colParentWidth - colMinWidth * 1.19 : colMinWidth;
                            const resultVerB = (colParentWidth>(numColsCounted+.24)*colMinWidth?colParentWidth:(numColsCounted+.24)*colMinWidth) / numColsCounted;
                            result = (resultVerA * resultVerB) ** .5;
                        }
                        return result;
                    })();
                    const colWidthsAverageAcrossSections = (function(){
                        const isValValid = val => isFinite(val) && (val>0);
                        var result = [];
                        for(let colIndex=0;colIndex<=colMaxIndex;++colIndex) {
                            var numSectionsCounted = 0;
                            if(!result[colIndex]) result[colIndex] = 0;
                            Array.prototype.forEach.call(tables_all,function(tableEl,tableIndex) {
                                const val = colWidthsData[colIndex][tableIndex];
                                if(isValValid(val)) {
                                    if(!result[colIndex]) result[colIndex] = 0;
                                    result[colIndex] += val;
                                    numSectionsCounted++;
                                }
                            });
                            result[colIndex] = numSectionsCounted>0 ? result[colIndex] / numSectionsCounted : 0;
                        }
                        return result;
                    })();
                    const colWidthsAdjusted = (function(){
                        const isValValid = val => isFinite(val) && (val>0);
                        var result = Array.from(colWidthsAverageAcrossSections);
                        const sum = result.reduce((acc,val)=>isValValid(val)?(acc+val):acc,0);
                        if( sum<colParentWidth ) {
                            /* const multiplier = (colParentWidth-0.00001) / sum; */
                            /* result = result.map(a=>a*multiplier); */
                            const isBig = a => a>widthDefault*.99;
                            const addPart = result.map(a=>({width:a,addCount:a>0?(isBig(a)?4:1):0}));
                            const multiplier = ( colParentWidth-0.00001 + addPart.reduce((acc,e)=>acc+colMinWidth*e.addCount,0) ) / addPart.reduce((acc,e)=>acc+e.width+colMinWidth*e.addCount,0);
                            if(!(multiplier>=1)) throw new Error('resizing columns: wrong multiplier');
                            result = addPart.map(a=>a.width*multiplier+colMinWidth*a.addCount*(multiplier-1));
                        }
                        result = result.map( a => a>=colMinWidth ? a : colMinWidth );
                        return result;
                    })();
                    (function(){
                        var cssSyntax = '';
                        for(colIndex=0;colIndex<=colMaxIndex;colIndex++) {
                            const colClass = `mdmreport-colindex-${colIndex}`;
                            const widthRaw = `${( isFinite(colWidthsAdjusted[colIndex]) && (colWidthsAdjusted[colIndex]>colMaxAllowedWidth) ? colMaxAllowedWidth : colWidthsAdjusted[colIndex] )}`;
                            const widthVal = `${widthRaw}px`;
                            cssSyntax = cssSyntax + ` .${colClass} { width: ${widthVal}!important; max-width: ${widthVal}!important; } `;
                        }
                        cssSheet.replaceSync(cssSyntax);
                    })();
                    Array.prototype.forEach.call(tables_all,function(tableEl,tableIndex) {
                        //const rowElements = tableEl.querySelectorAll('tr.mdmreport-record');
                        //Array.prototype.forEach.call(rowElements,function(rowElement,tableIndex) {
                        //    colElements = rowElement.querySelectorAll('tr.mdmreport-record>td');
                        //    Array.prototype.forEach.call(colElements,function(colEl,colIndex) {
                        //        colEl.width = colWidthsAdjusted[colIndex];
                        //    });
                        //});
                        tableEl.classList.add('mdmreport-table-formatting-fixeddimensions');
                    });
                } catch(e) {
                    try {
                        function escapeHtml(s) {
                            const dummy = document.createElement('div');
                            dummy.innerText = s.replace(/\n/ig,'\\n');
                            return dummy.innerHTML;
                        }
                        errorBannerEl.innerHTML = errorBannerEl.innerHTML + escapeHtml(`Error: Error when resizing columns: ${e}`)+'<br />';
                    } catch(ee) {};
                    try {
                        document.removeEventListener('DOMContentLoaded',alignColWidths);
                    } catch(ee) {}
                    throw e;
                }
            };
            Promise.resolve().then(process);
            const dispatchDelayedEventData = {
                promise: null
            };
            function processDelayed() {
                if(!!dispatchDelayedEventData.promise) {
                    /* setTimeout(resolve,40); */
                } else {
                    dispatchDelayedEventData.promise = new Promise((resolve,reject)=>{
                        setTimeout(resolve,40);
                    });
                    dispatchDelayedEventData.promise.then(()=>{
                        dispatchDelayedEventData.promise = null;
                        return process();
                    });
                }
            }
            window.addEventListener('resize',processDelayed);
            window.addEventListener('mdmreport_table',processDelayed);
            document.removeEventListener('DOMContentLoaded',alignColWidths);
        } catch(e) {
            try {
                function escapeHtml(s) {
                    const dummy = document.createElement('div');
                    dummy.innerText = s.replace(/\n/ig,'\\n');
                    return dummy.innerHTML;
                }
                errorBannerEl.innerHTML = errorBannerEl.innerHTML + escapeHtml(`Error: ${e}`)+'<br />';
            } catch(ee) {};
            try {
                document.removeEventListener('DOMContentLoaded',alignColWidths);
            } catch(ee) {}
            throw e;
        }
    }
    window.addEventListener('DOMContentLoaded',alignColWidths);
})()
</script>
<script>
    /* === show/hide columns js === */
(function() {
    const globalDataStored = {};
    const cssSheet = new CSSStyleSheet();
    function decideColumnsShownAtStartup(columnIDs,addedData) {
        function normalizeSectionId(id) {
            return id.replace(/_/ig,' ').replace(/\s/ig,' ').replace(/\bx\d+\b/ig,' ').replace(/\s+/ig,' ').replace(/^\s*/ig,'').replace(/\s*$/ig,'');
        }
        const columns = new Set(columnIDs);
        if(Array.from(columns).length==0) {
            return Array.from(columns);
        }
        const sectionNames = addedData.sectionNames.map(normalizeSectionId)
        function setDifference(a,b){/* something is not working with Sets in my chrome, strange - adding this helper fn to find differences as between arrays */  return new Set(Array.from(a).filter(function(ai){return !Array.from(b).includes(ai);})); }
        const columns_subsetName = new Set(columnIDs.filter(function(id){return /^\s*?name\s*?$/.test(id)}));
        const columns_subsetFlag = new Set(columnIDs.filter(function(id){return /^\s*?flag.*\s*?$/.test(id)}));
        const columns_subsetLabel = new Set(columnIDs.filter(function(id){return /^\s*?label\w*\s*?$/.test(id)}));
        const columns_subsetProperties = new Set(columnIDs.filter(function(id){return /^\s*?properties\w*\s*?$/.test(id)}));
        const columns_subsetAttributes = new Set(columnIDs.filter(function(id){return /^\s*?attributes\w*\s*?$/.test(id)}));
        const columns_subsetTranslations = new Set(columnIDs.filter(function(id){return /^\s*?langcode.*\s*?$/.test(id)}));
        const columns_subsetScripting = new Set(columnIDs.filter(function(id){return /^\s*?script\w*\s*?$/.test(id)}));
        const columns_subsetRawText = new Set(columnIDs.filter(function(id){return /^\s*?rawtext\w*\s*?$/.test(id)}));
        if( ( (Array.from(sectionNames)).includes('routing') ) && ( Array.from(setDifference(sectionNames,['routing']))==0 ) ) {
            if(Array.from(columns_subsetLabel).length>0) {
                return Array.from(columns_subsetLabel);
            }
        }
        if( ( Array.from(sectionNames).length==1 ) && ( Array.from(columns_subsetRawText).length>0 ) ) {
            if(Array.from(columns_subsetRawText).length>0) {
                const statisticsNumRows = (function(){
                    const sectionsMatching = addedData.sectionDefs.filter(()=>true);
                    if(sectionsMatching.length==1) {
                        const section = sectionsMatching[0];
                        const statisticsText = !!section.statisticsText ? section.statisticsText : '';
                        if(!!statisticsText && statisticsText.trim().length>0 ) {
                            const matches = Array.from(statisticsText.matchAll( /\brows\b\s*?\btotal\s*?:\s*?(\d+)\b,/ig ));
                            if( matches.length>0 ) {
                                const resultTxt = matches[0][1];
                                return +resultTxt;
                            }
                        }
                    } /* else return NaN */;
                    return NaN;
                })();
                if( isFinite(statisticsNumRows) && statisticsNumRows==1 ) {
                    return Array.from(columns_subsetRawText);
                } else {
                    return [...columns_subsetFlag,...columns_subsetRawText];
                }
            }
        }
        if( ((addedData.columnDefs.filter(a=>(a.id=='name')&&(a.text=='Row unique indentifier'))).length>0) && ((addedData.columnDefs.filter(a=>(/^\s*?axis\s*?\(\s*?side\s*?\).*?/.test(a.text)))).length>0) ) {
            return Array.from(setDifference( columns, columns_subsetName ))
        }
        if( (addedData.sectionDefs.map(a=>a.text).filter(a=>(/.*?(?:shared[_\s]+list|(?:\bfield(?:s)?\b)).*?/.test(a))).length>0) && ( (Array.from(columns_subsetName)).length>0 ) && ( (Array.from(columns_subsetLabel)).length>0 ) ) {
            const result_TranslationsExcluded = setDifference( columns, columns_subsetTranslations )
            if(Array.from(result_TranslationsExcluded).length>0) {
                const result_ScriptingTranslationsExcluded = setDifference( result_TranslationsExcluded, columns_subsetScripting )
                if(Array.from(result_ScriptingTranslationsExcluded).length>0) {
                    return Array.from(result_ScriptingTranslationsExcluded);
                } else {
                    return Array.from(result_TranslationsExcluded);
                }
            }
        }
        return Array.from(columns);
    }
    function addControlBlock_ShowHideColumns() {
        let errorBannerEl = null;
        try {
            errorBannerEl = document.querySelector('#error_banner');
            if( !errorBannerEl ) throw new Error('no error banner, stop execution of js scripts');
        } catch(e) {
            throw e;
            return;
        }
        try {
            // 1. read data and find the list of columns in the report table
            // it's interesting, we don't care how many columns are there; we iterate over css classes, and adding show/hide functionality per css class
            // so, if 2 classes are added to a cell, there would be 2 checkboxes, and if there is a column missing necessary class, there would be no check box
            const columns = [];
            const columnTitles = {};
            const sectionEls = document.querySelectorAll('table.mdmreport-table');
            Array.from(sectionEls).forEach(function(sectionEl){
                const rowContainingColsElements = sectionEl.querySelectorAll('tr.mdmreport-record');
                Array.from(rowContainingColsElements).filter(function(e,i){return i==0;}).forEach(function(rowRefEl){
                    const colElements = rowRefEl.querySelectorAll('td.mdmreport-contentcell');
                    Array.prototype.forEach.call(colElements,function(colEl) {
                        const cssClasses = Array.from(colEl.classList);
                        const cssClassesMatching = cssClasses.filter(function(n) {return /^\s*?(mdmreport-col-)(.*?)\s*?$/ig.test(n);});
                        cssClassesMatching.map(function(n) {return n.replace(/^\s*?(mdmreport-col-)(.*?)\s*?$/ig,'$2');}).forEach(function(colNameFromCSS) {
                            const colName = colNameFromCSS;
                            //colName = colName.replace(/^\s*/,'').replace(/\s*$/,'');
                            const colTitlesAllOfThisCssClass = Array.from(rowRefEl.querySelectorAll(`.mdmreport-col-${colName}`)).map(el=>el.textContent);
                            const colTitlesNoDuplicates = colTitlesAllOfThisCssClass.reduce(function(acc,val){if(acc.includes(val))return acc; else return [...acc,val];},[]);
                            const colTitle = colTitlesNoDuplicates.length==1 ? colTitlesNoDuplicates[0] : `${colEl.textContent} (${colName})`;
                            if( columns.includes(colName) ) {
                                /* skip - already on the list */
                            } else {
                                columnTitles[colName] = colTitle;
                                columns.push(colName);
                            }
                        });
                    });
                });
            });
            // 2. add a control block
            function applyDefaultSetup(listOfControls) {
                // input: array of {id:colClassName,text:colText,controlEl:checkboxEl}
                // expected behaviour: check/uncheck listOfControls[..].controlEl
                // not a clean fn
                try {
                    columnsAll = listOfControls.map(function(a){return a.id});
                    const sectionElements = document.querySelectorAll('[class^="mdmreport-wrapper-section-"], [class*=" mdmreport-wrapper-section-"]');
                    const sectionDefs = Array.from(sectionElements).map(function(sectionElement){
                        var textTitle = `${(sectionElement.querySelector('h3') || {textContent:''}).textContent}`.replace(/^\s*?section\s+/ig,'');
                        var textCss = ( Array.from(sectionElement.classList).filter(function(name){return /^\s*?mdmreport-wrapper-section-/ig.test(name)}) || [''] )[0].replace(/^\s*?mdmreport-wrapper-section-/ig,'');
                        textTitle = textTitle.replace(/^\s*(.*?)\s*$/ig,'$1');
                        /* trim */ textCss = textCss.replace(/^\s*(.*?)\s*$/ig,'$1');
                        /* trim */ if( ( !!textTitle && (textTitle.length>0) ) || ( !!textCss && (textCss.length>0) ) ) {
                            if( !textTitle || (textTitle.length==0) ) textTitle = textCss;
                            if( !textCss || (textCss.length==0) ) textCss = textTitle; textCss = textCss.replace(/[^\w\-\.]/ig,'-');
                        }
                        const statisticsEl = sectionElement.querySelector('.mdmreport-banner-table-details-statistics');
                        const statisticsText = !!statisticsEl && (`${statisticsEl.innerText}`.trim().length>0) ? `${statisticsEl.innerText}`.trim() : null;
                        return {
                            text: textTitle,
                            id: textCss,
                            name: textCss,
                            statisticsText: statisticsText,
                            el: sectionElement
                        };
                    });
                    const meta = [];
                    const addedData = {
                        columnDefs: listOfControls,
                        sectionNames: sectionDefs.map(a=>a.name),
                        sectionDefs: sectionDefs,
                        meta: meta
                    };
                    columnsShown = decideColumnsShownAtStartup(columnsAll,addedData).filter( hid => (!Object.keys(globalDataStored).includes(hid) || (Object.keys(globalDataStored).filter(id=>!!globalDataStored[id]).includes(hid)) ) ).concat( Object.keys(globalDataStored).filter(id=>!!globalDataStored[id]) );
                    columnsAll.forEach(function(columnId){
                        const d = listOfControls.filter(function(def){ return def.id==columnId; })[0];
                        const isShown = columnsShown.includes(columnId);
                        if( isShown ) {
                            d.controlEl.checked = true;
                            d.controlEl.dispatchEvent(new Event('change'));
                        } else {
                            d.controlEl.checked = false;
                            d.controlEl.dispatchEvent(new Event('change'));
                        }
                    });
                } catch(e) {
                    try {
                        function escapeHtml(s) {
                            const dummy = document.createElement('div');
                            dummy.innerText = s.replace(/\n/ig,'\\n');
                            return dummy.innerHTML;
                        }
                        errorBannerEl.innerHTML = errorBannerEl.innerHTML + escapeHtml(`Error: ${e}`)+'<br />';
                    } catch(ee) {};
                    throw e;
                }
            }
            function initSettingCss() {
                // .mdmreport-hidecol-xxx .mdmreport-col-xxx
                const cssSyntax = columns.map(function(item) {
                    const itemClassName = item.replace(/[^\w\-\.]/ig,'');
                    return ' .mdmreport-hidecol-xxx .mdmreport-col-xxx { display: none; } '.replaceAll('xxx',itemClassName);
                }).join('');
                cssSheet.replaceSync(cssSyntax);
                document.adoptedStyleSheets = [...document.adoptedStyleSheets,cssSheet];
            }
            const dispatchResizeEventData = {
                promise: null
            };
            function dispatchResizeEvent() {
                if(!!dispatchResizeEventData.promise) {
                    /* setTimeout(resolve,40); */
                } else {
                    dispatchResizeEventData.promise = new Promise((resolve,reject)=>{
                        setTimeout(resolve,40);
                    });
                    dispatchResizeEventData.promise.then(()=>{
                        window.dispatchEvent(new Event('resize'));
                        dispatchResizeEventData.promise = null;
                    });
                }
            }
            function initAddingControlBlock() {
                const pluginHolderEl = document.querySelector('#mdmreport_plugin_placeholder');
                if(!pluginHolderEl) throw new Error('adding block to show/hide columns: failed to find proper place for the element: #mdmreport_plugin_placeholder');
                const bannerEl = document.createElement('div');
                bannerEl.className = 'mdmreport-showhidecolumns-plugin mdmreport-banner mdmreport-banner-columns';
                bannerEl.innerHTML = '<form method="_POST" action="#!" onSubmit="javascript: return false;" class="mdmreport-controls"><fieldset class="mdmreport-controls"><div><legend>Show/hide columns:</legend></div></fieldset></form>';
                Array.prototype.forEach.call(bannerEl.querySelectorAll('form'),function(formEl) {formEl.addEventListener('submit',function(event) {event.preventDefault();event.stopPropagation();return false;});});
                const possiblyExistingEl = document.querySelector('.mdmreport-showhidecolumns-plugin');
                if( columns.length==0 ) {
                    /* nothing */
                } else {
                    if( possiblyExistingEl ) {
                        possiblyExistingEl.replaceWith(bannerEl);
                    } else {
                        pluginHolderEl.append(bannerEl);
                    }
                }
                controlsDefs = [];
                columns.forEach(function(col) {
                    try {
                        const colText = columnTitles[col];
                        const colClassName = col.replace(/[^\w\-\.]/ig,'');
                        const labelEl = document.createElement('label');
                        labelEl.textContent = colText;
                        labelEl.classList.add('mdmreport-controls');
                        const checkboxEl = document.createElement('input');
                        checkboxEl.setAttribute('type','checkbox');
                        checkboxEl.setAttribute('checked','true');
                        checkboxEl.checked = true;
                        checkboxEl.addEventListener('change',function(event) {
                            const checkboxEl = event.target;
                            const className = `mdmreport-hidecol-${colClassName}`; // mdmreport-col-xxx
                            globalDataStored[colClassName] = !!checkboxEl.checked;
                            if( checkboxEl.checked ) {
                                Array.prototype.forEach.call(document.querySelectorAll('table.mdmreport-table'),function(tableEl) {
                                    tableEl.classList.remove(className);
                                });
                            } else {
                                Array.prototype.forEach.call(document.querySelectorAll('table.mdmreport-table'),function(tableEl) {
                                    tableEl.classList.add(className);
                                });
                            };
                            dispatchResizeEvent();
                        });
                        labelEl.prepend(checkboxEl);
                        bannerEl.querySelector('fieldset').append(labelEl);
                        controlsDefs.push({id:colClassName,text:colText,controlEl:checkboxEl});
                    } catch(e) {
                        try {
                            function escapeHtml(s) {
                                const dummy = document.createElement('div');
                                dummy.innerText = s.replace(/\n/ig,'\\n');
                                return dummy.innerHTML;
                            }
                            errorBannerEl.innerHTML = errorBannerEl.innerHTML + escapeHtml(`Error: ${e}`)+'<br />';
                        } catch(ee) {};
                        throw e;
                    }
                });
            }
            initSettingCss();
            initAddingControlBlock();
            setTimeout(function(){ applyDefaultSetup(controlsDefs); },50);
            document.removeEventListener('DOMContentLoaded',addControlBlock_ShowHideColumns);
        } catch(e) {
            try {
                function escapeHtml(s) {
                    const dummy = document.createElement('div');
                    dummy.innerText = s.replace(/\n/ig,'\\n');
                    return dummy.innerHTML;
                }
                errorBannerEl.innerHTML = errorBannerEl.innerHTML + escapeHtml(`Error: ${e}`)+'<br />';
            } catch(ee) {};
            try {
                document.removeEventListener('DOMContentLoaded',addControlBlock_ShowHideColumns);
            } catch(ee) {}
            throw e;
        }
    }
    window.addEventListener('DOMContentLoaded',addControlBlock_ShowHideColumns);
    /* window.mdmreportPluginShowHideColsInit = addControlBlock_ShowHideColumns; */
    window.addEventListener('mdmreport_table',addControlBlock_ShowHideColumns);
})()
</script>
<style>
    /* === column filtering css === */
.mdmreport-record.mdmreport-tablefilterplugin-hide-0, .mdmreport-record.mdmreport-tablefilterplugin-hide-1, .mdmreport-record.mdmreport-tablefilterplugin-hide-2, .mdmreport-record.mdmreport-tablefilterplugin-hide-3, .mdmreport-record.mdmreport-tablefilterplugin-hide-4, .mdmreport-record.mdmreport-tablefilterplugin-hide-5, .mdmreport-record.mdmreport-tablefilterplugin-hide-6, .mdmreport-record.mdmreport-tablefilterplugin-hide-7, .mdmreport-record.mdmreport-tablefilterplugin-hide-8, .mdmreport-record.mdmreport-tablefilterplugin-hide-9, .mdmreport-record.mdmreport-tablefilterplugin-hide-10, .mdmreport-record.mdmreport-tablefilterplugin-hide-11, .mdmreport-record.mdmreport-tablefilterplugin-hide-12, .mdmreport-record.mdmreport-tablefilterplugin-hide-13, .mdmreport-record.mdmreport-tablefilterplugin-hide-14, .mdmreport-record.mdmreport-tablefilterplugin-hide-15, .mdmreport-record.mdmreport-tablefilterplugin-hide-16, .mdmreport-record.mdmreport-tablefilterplugin-hide-17, .mdmreport-record.mdmreport-tablefilterplugin-hide-18, .mdmreport-record.mdmreport-tablefilterplugin-hide-19, .mdmreport-record.mdmreport-tablefilterplugin-hide-20, .mdmreport-record.mdmreport-tablefilterplugin-hide-21, .mdmreport-record.mdmreport-tablefilterplugin-hide-22, .mdmreport-record.mdmreport-tablefilterplugin-hide-23, .mdmreport-record.mdmreport-tablefilterplugin-hide-24, .mdmreport-record.mdmreport-tablefilterplugin-hide-25, .mdmreport-record.mdmreport-tablefilterplugin-hide-26, .mdmreport-record.mdmreport-tablefilterplugin-hide-27, .mdmreport-record.mdmreport-tablefilterplugin-hide-28, .mdmreport-record.mdmreport-tablefilterplugin-hide-29, .mdmreport-record.mdmreport-tablefilterplugin-hide-30, .mdmreport-record.mdmreport-tablefilterplugin-hide-31, .mdmreport-record.mdmreport-tablefilterplugin-hide-32, .mdmreport-record.mdmreport-tablefilterplugin-hide-33, .mdmreport-record.mdmreport-tablefilterplugin-hide-34, .mdmreport-record.mdmreport-tablefilterplugin-hide-35, .mdmreport-record.mdmreport-tablefilterplugin-hide-36, .mdmreport-record.mdmreport-tablefilterplugin-hide-37, .mdmreport-record.mdmreport-tablefilterplugin-hide-38, .mdmreport-record.mdmreport-tablefilterplugin-hide-39, .mdmreport-record.mdmreport-tablefilterplugin-hide-40, .mdmreport-record.mdmreport-tablefilterplugin-hide-41, .mdmreport-record.mdmreport-tablefilterplugin-hide-42, .mdmreport-record.mdmreport-tablefilterplugin-hide-43, .mdmreport-record.mdmreport-tablefilterplugin-hide-44, .mdmreport-record.mdmreport-tablefilterplugin-hide-45, .mdmreport-record.mdmreport-tablefilterplugin-hide-46, .mdmreport-record.mdmreport-tablefilterplugin-hide-47, .mdmreport-record.mdmreport-tablefilterplugin-hide-48, .mdmreport-record.mdmreport-tablefilterplugin-hide-49, .mdmreport-record.mdmreport-tablefilterplugin-hide-50, .mdmreport-record.mdmreport-tablefilterplugin-hide-51, .mdmreport-record.mdmreport-tablefilterplugin-hide-52, .mdmreport-record.mdmreport-tablefilterplugin-hide-53, .mdmreport-record.mdmreport-tablefilterplugin-hide-54, .mdmreport-record.mdmreport-tablefilterplugin-hide-55, .mdmreport-record.mdmreport-tablefilterplugin-hide-56, .mdmreport-record.mdmreport-tablefilterplugin-hide-57, .mdmreport-record.mdmreport-tablefilterplugin-hide-58, .mdmreport-record.mdmreport-tablefilterplugin-hide-59, .mdmreport-record.mdmreport-tablefilterplugin-hide-60, .mdmreport-record.mdmreport-tablefilterplugin-hide-61, .mdmreport-record.mdmreport-tablefilterplugin-hide-62, .mdmreport-record.mdmreport-tablefilterplugin-hide-63, .mdmreport-record.mdmreport-tablefilterplugin-hide-64, .mdmreport-record.mdmreport-tablefilterplugin-hide-65, .mdmreport-record.mdmreport-tablefilterplugin-hide-66, .mdmreport-record.mdmreport-tablefilterplugin-hide-67, .mdmreport-record.mdmreport-tablefilterplugin-hide-68, .mdmreport-record.mdmreport-tablefilterplugin-hide-69, .mdmreport-record.mdmreport-tablefilterplugin-hide-70, .mdmreport-record.mdmreport-tablefilterplugin-hide-71, .mdmreport-record.mdmreport-tablefilterplugin-hide-72, .mdmreport-record.mdmreport-tablefilterplugin-hide-73, .mdmreport-record.mdmreport-tablefilterplugin-hide-74, .mdmreport-record.mdmreport-tablefilterplugin-hide-75, .mdmreport-record.mdmreport-tablefilterplugin-hide-76, .mdmreport-record.mdmreport-tablefilterplugin-hide-77, .mdmreport-record.mdmreport-tablefilterplugin-hide-78, .mdmreport-record.mdmreport-tablefilterplugin-hide-79, .mdmreport-record.mdmreport-tablefilterplugin-hide-80, .mdmreport-record.mdmreport-tablefilterplugin-hide-81, .mdmreport-record.mdmreport-tablefilterplugin-hide-82, .mdmreport-record.mdmreport-tablefilterplugin-hide-83, .mdmreport-record.mdmreport-tablefilterplugin-hide-84, .mdmreport-record.mdmreport-tablefilterplugin-hide-85, .mdmreport-record.mdmreport-tablefilterplugin-hide-86, .mdmreport-record.mdmreport-tablefilterplugin-hide-87, .mdmreport-record.mdmreport-tablefilterplugin-hide-88, .mdmreport-record.mdmreport-tablefilterplugin-hide-89, .mdmreport-record.mdmreport-tablefilterplugin-hide-90, .mdmreport-record.mdmreport-tablefilterplugin-hide-91, .mdmreport-record.mdmreport-tablefilterplugin-hide-92, .mdmreport-record.mdmreport-tablefilterplugin-hide-93, .mdmreport-record.mdmreport-tablefilterplugin-hide-94, .mdmreport-record.mdmreport-tablefilterplugin-hide-95, .mdmreport-record.mdmreport-tablefilterplugin-hide-96, .mdmreport-record.mdmreport-tablefilterplugin-hide-97, .mdmreport-record.mdmreport-tablefilterplugin-hide-98, .mdmreport-record.mdmreport-tablefilterplugin-hide-99 {
    display: none!important;
}
tr.mdmreport-record td.mdmreport-contentcell.mdmreport-tablefilterplugin-enchancedcell {
    padding-bottom: 2.55em;
    position: relative;
}
td.mdmreport-contentcell .mdmreport-tablefilterplugin-controls {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 2px; /* to align with that green bottom border */
    /* height: 1.9em; */
    padding: 0; /* .1em; */
    /* line-height: 1em;
    padding: 0.35em; */
}
</style>
<script>
    /* === column filtering js === */
(function() {
    function addElementsToTables_TableFilters() {
        let errorBannerEl = null;
        try {
            errorBannerEl = document.querySelector('#error_banner');
            if( !errorBannerEl ) throw new Error('no error banner, stop execution of js scripts');
        } catch(e) {
            throw e;
            return;
        }
        function bubbleException(e) {
            try {
                function escapeHtml(s) {
                    const dummy = document.createElement('div');
                    dummy.innerText = s.replace(/\n/ig,'\\n');
                    return dummy.innerHTML;
                }
                errorBannerEl.innerHTML = errorBannerEl.innerHTML + escapeHtml(`Error: ${e}`)+'<br />';
            } catch(ee) {};
            throw e;
        }
        try {
            // 1. read data and find the list of sections in the report table
            const sectionElements = document.querySelectorAll('[class^="mdmreport-wrapper-section-"], [class*=" mdmreport-wrapper-section-"]');
            Array.prototype.forEach.call(sectionElements,function(sectionElement) {
                if( sectionElement.querySelector('.mdmreport-tablefilterplugin-controls') )
                    return;
                var textTitle = `${(sectionElement.querySelector('h3') || {textContent:''}).textContent}`.replace(/^\s*?section\s+/ig,'');
                const sectionClasses = Array.from(sectionElement.classList).filter(function(name){return /^\s*?mdmreport-wrapper-section-/ig.test(name)});
                const sectionClassesUnique = sectionClasses.filter(function(className){return document.querySelectorAll('.'+className).length==1});
                if( !(sectionClassesUnique.length>0) ) return;
                const sectionClass = sectionClassesUnique[0];
                var textCss = sectionClass.replace(/^\s*?mdmreport-wrapper-section-/ig,'');
                textTitle = textTitle.replace(/^\s*(.*?)\s*$/ig,'$1'); // trim
                textCss = textCss.replace(/^\s*(.*?)\s*$/ig,'$1'); // trim
                if( !( ( !!textTitle && (textTitle.length>0) ) || ( !!textCss && (textCss.length>0) ) ) ) return;
                if( !textTitle || (textTitle.length==0) ) textTitle = textCss;
                if( !textCss || (textCss.length==0) ) textCss = textTitle;
                textCss = textCss.replace(/[^\w\-\.]/ig,'-');
                const sectionDef = {
                    text:textTitle,
                    id:textCss,
                    tableElement:sectionElement.querySelector('table.mdmreport-table'),
                    sectionClass: sectionClass
                    };
                if(!sectionDef.tableElement) return;
                const headerRowEls = sectionDef.tableElement.querySelectorAll('tr.mdmreport-record-header');
                const allRows = Array.from(sectionDef.tableElement.querySelectorAll('tr.mdmreport-record:not(.mdmreport-record-header)')).map(function(element,index) {
                    const texts = Array.from(element.querySelectorAll('td.mdmreport-contentcell')).map(function(el){
                        var result = el.innerText||el.textContent;
                        if( el.hasAttribute('data-added') )
                            result = result + ' ' + el.getAttribute('data-added');
                        Array.from(el.querySelectorAll('[data-added]')).forEach(function(el){
                            result = result + ' ' + el.getAttribute('data-added');
                        });
                        return result;
                    });
                    return {element,texts,index};
                });
                if(!(headerRowEls.length>0)) return;
                const headerRowEl = headerRowEls[0];
                const cellElements = headerRowEl.querySelectorAll('td.mdmreport-contentcell');
                Array.from(cellElements).forEach(function(cellEl,colIndex){
                    const controlGroupElAdd = document.createElement('div');
                    controlGroupElAdd.className = 'mdmreport-tablefilterplugin-controls';
                    controlGroupElAdd.innerHTML = '<fieldset class="mdmreport-controls"><div class="mdmreport-controls-group"><input type="text" value="" placeholder="type something to filter..." /></div></fieldset>';
                    const controlEl = controlGroupElAdd.querySelector('input');
                    function doFilter() {
                        const checkStr = controlEl.value;
                        allRows.forEach(function(rowDef) {
                            function doesCellMatchFilter(cellContents,checkStr){
                                return cellContents.toLowerCase().includes(checkStr.toLowerCase());
                            }
                            const cellContents = rowDef.texts[colIndex];
                            const isMatching = (checkStr.length==0) || doesCellMatchFilter(cellContents,checkStr);
                            const cssControlClass = `mdmreport-tablefilterplugin-hide-${colIndex}`;
                            if(isMatching)
                                rowDef.element.classList.remove(cssControlClass);
                            else
                                rowDef.element.classList.add(cssControlClass);
                        });
                    }
                    const promiseState = {
                        active: false
                    };
                    function doFilterDelayed() {
                        if(promiseState.active) {
                            // just keep going
                        } else {
                            promiseState.active = true;
                            const promise = new Promise(function(resolve,reject){setTimeout(resolve,100);});
                            promise.then(function() {
                                try {
                                    promiseState.active = false;
                                    doFilter();
                                } catch(e) {
                                    bubbleException(e);
                                    throw e;
                                }
                            });
                        }
                    }
                    function handleChange(event) {
                        try {
                            //event.preventDefault();
                            //event.stopPropagation();
                            doFilterDelayed();
                            //return false;
                        } catch(e) {
                            bubbleException(e);
                            throw e;
                        }
                    }
                    controlEl.addEventListener('change',handleChange);
                    controlEl.addEventListener('keyup',handleChange);
                    controlEl.addEventListener('keydown',handleChange);
                    controlEl.addEventListener('keypress',handleChange);
                    cellEl.append(controlGroupElAdd);
                    cellEl.classList.add('mdmreport-tablefilterplugin-enchancedcell');
                });
            });
        } catch(e) {
            try {
                function escapeHtml(s) {
                    const dummy = document.createElement('div');
                    dummy.innerText = s.replace(/\n/ig,'\\n');
                    return dummy.innerHTML;
                }
                errorBannerEl.innerHTML = errorBannerEl.innerHTML + escapeHtml(`Error: ${e}`)+'<br />';
            } catch(ee) {};
            throw e;
        }
    }
    function addControlBlock_TableFilters() {
        let errorBannerEl = null;
        try {
            errorBannerEl = document.querySelector('#error_banner');
            if( !errorBannerEl ) throw new Error('no error banner, stop execution of js scripts');
        } catch(e) {
            throw e;
            return;
        }
        try {
            // 2. add a control block
            function initAddingControlBlock() {
                const pluginHolderEl = document.querySelector('#mdmreport_plugin_placeholder');
                if(!pluginHolderEl) throw new Error('adding block with table filters: failed to find proper place for the element: #mdmreport_plugin_placeholder');
                const bannerEl = document.createElement('div');
                bannerEl.className = 'mdmreport-tablefilters-plugin mdmreport-banner mdmreport-banner-tablefilters';
                bannerEl.innerHTML = '<form method="_POST" action="#!" onSubmit="javascript: return false;" class="mdmreport-controls"><fieldset class="mdmreport-controls"><div><legend>Add the ability to filter tables by content</legend></div><input type="submit" value="Yes, add this please!" /></fieldset></form>';
                Array.prototype.forEach.call(bannerEl.querySelectorAll('form'),function(formEl) {formEl.addEventListener('submit',function(event) {
                    try {
                        event.preventDefault();
                        event.stopPropagation();
                        addElementsToTables_TableFilters();
                        //bannerEl.classList.add('mdmreport-format-hidden');
                        bannerEl.innerHTML = '<p>Add the ability to filter tables by content</p><span>Done, input boxes are added below the header line in every table.</span>';
                        return false;
                    } catch(e) {
                        try {
                            function escapeHtml(s) {
                                const dummy = document.createElement('div');
                                dummy.innerText = s.replace(/\n/ig,'\\n');
                                return dummy.innerHTML;
                            }
                            errorBannerEl.innerHTML = errorBannerEl.innerHTML + escapeHtml(`Error: ${e}`)+'<br />';
                        } catch(ee) {};
                        throw e;
                    }
                });});
                // pluginHolderEl.append(bannerEl); // we don't want the user to press "add", we are just adding it, it's so nice to have, it is now added automatically
                setTimeout(addElementsToTables_TableFilters,400);
                window.addEventListener('mdmreport_table',addElementsToTables_TableFilters);
            }
            initAddingControlBlock();
            document.removeEventListener('DOMContentLoaded',addControlBlock_TableFilters);
        } catch(e) {
            try {
                function escapeHtml(s) {
                    const dummy = document.createElement('div');
                    dummy.innerText = s.replace(/\n/ig,'\\n');
                    return dummy.innerHTML;
                }
                errorBannerEl.innerHTML = errorBannerEl.innerHTML + escapeHtml(`Error: ${e}`)+'<br />';
            } catch(ee) {};
            try {
                document.removeEventListener('DOMContentLoaded',addControlBlock_TableFilters);
            } catch(ee) {}
            throw e;
        }
    }
    window.addEventListener('DOMContentLoaded',addControlBlock_TableFilters);
})()
</script>
<style>
.toc-section-row {
    margin-left: -0.65em;
}
.mdmreport-showhidesections-plugin .toc-section-row .toc-section-plainlink {
    display: none;
}
.mdmreport-showhidesections-plugin .toc-section-row .toc-section-hyperlink {
    display: inline-block;
}
.mdmreport-showhidesections-plugin .toc-section-row.toc-section-inactive .toc-section-plainlink {
    display: inline-block;
}
.mdmreport-showhidesections-plugin .toc-section-row.toc-section-inactive .toc-section-hyperlink {
    display: none;
}
.toc-section-highlighted {
    background: #ffe49c;
}
.mdmreport-showhidesections-plugin .toc-statistics {
    display: inline-block;
    color: rgba(0,0,0,.5);
    padding-left: 1em;
    max-width: 100%;
    text-overflow: ellipsis;
    overflow-x: hidden;
    line-height: 1.1em;
    white-space: nowrap;
    vertical-align: middle;
}
.toc-statistics .mdmdiff-inlineoverlay-added {
    color: #000;
    background: transparent;
    text-decoration: underline;
}
</style>
<style>
    .mdmreport-plugin-validate-labels-error { color: #900; font-weight: 600; }
    .mdmreport-plugin-validate-labels { }
    .mdmreport-plugin-validate-labels-validated { }
    .mdmreport-plugin-validate-labels-alertissues, .mdmrep-plgn-labelxmlerr { text-decoration-line: underline; text-decoration-style: dashed; text-decoration-color: #db4069; text-decoration-offset: 2px; }
</style>
"""


TEMPLATE_HTML_COPYBANNER = r"""
AP
    """

TEMPLATE_HTML_TABLE_BEGIN = r"""
<div class="wrapper mdmreport-section-wrapper mdmreport-wrapper-section-{{TABLE_ID}}">
<h3 class="mdmreport-table-title">Section {{TABLE_NAME}}</h3>{{INS_TABBANNER}}
<div class="mdmreport-table-wrapper"><table class="mdmreport-table mdmreport-table-section-{{TABLE_ID}}"><tbody>
"""

TEMPLATE_HTML_TABLE_END = r"""
</tbody></table></div></div>
"""

TEMPLATE_HTML_BEGIN = r"""

<!doctype html>
<html lang="">
<head>
      <meta charset="UTF-8">
      <meta http-equiv="X-UA-Compatible" content="IE=edge">
      <meta name="viewport" content="width=device-width">
      <title>{{{{INS_TITLE}}}}</title>
      <style>{TEMPLATE_HTML_CSS_NORMALIZECSS}</style>
      <style>
      {TEMPLATE_HTML_STYLES}
      {TEMPLATE_HTML_STYLES_TABLE}
      </style>
      <script>window.reportType = '{{{{INS_REPORTTYPE}}}}';</script>
      {ADD_SCRIPTS}
</head>
<body class="mdmreportpage mdmreportpage-type-{{{{INS_REPORTTYPE}}}}">
<header class="header">
    <div class="container">
        <p>{{{{INS_PAGEHEADER}}}}</p>
    </div>
</header>
<div class="main">
    <div class="container">
        <h1>{{{{INS_HEADING}}}}</h1>
        <div class="mdmreport-banner mdmreport-banner-global">{{{{INS_BANNER}}}}</div>
        <div class="error error-banner" id="error_banner"></div>
        <div class="mdmreport-layout-plugin-placeholder mdmreport-banners-wrapper" id="mdmreport_plugin_placeholder"></div><div class="mdmreport-toc-placeholder mdmreport-banners-wrapper mdmreport-banners-wrapper-noborders" id="mdmreport_toc_placeholder"></div><h2 style="display: none;">Sections</h2>
    """.format(
        TEMPLATE_HTML_CSS_NORMALIZECSS = TEMPLATE_HTML_CSS_NORMALIZECSS,
        TEMPLATE_HTML_STYLES = TEMPLATE_HTML_STYLES,
        TEMPLATE_HTML_STYLES_TABLE = TEMPLATE_HTML_STYLES_TABLE,
        ADD_SCRIPTS = '{allscripts}'.format(allscripts=TEMPLATE_HTML_SCRIPTS),
        # INS_TITLE = fields_File_INS_TITLE,
        # INS_REPORTTYPE = fields_INS_REPORTTYPE,
        # INS_HEADING = fields_File_INS_HEADING,
        # INS_BANNER = ''.join( [ '<p>{content}</p>'.format(content=preptext_html(content)) for content in fields_File_ReportInfo ] )
    )

TEMPLATE_HTML_END = r"""
        </div>
    </div>
    <footer class="footer">
        <div class="container">{TEMPLATE_HTML_COPYBANNER}</div>
    </footer>
</body>
</html>
    """.format(
        TEMPLATE_HTML_COPYBANNER = TEMPLATE_HTML_COPYBANNER
    )
