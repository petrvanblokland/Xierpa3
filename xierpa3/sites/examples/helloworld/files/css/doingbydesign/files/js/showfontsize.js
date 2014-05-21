function elementCurrentStyle(element, styleName){
    if (element.currentStyle){
        var i = 0, temp = "", changeCase = false;
        for (i = 0; i < styleName.length; i++)
            if (styleName[i] != '-'){
                temp += (changeCase ? styleName[i].toUpperCase() : styleName[i]);
                changeCase = false;
            } else {
                changeCase = true;
            }
        styleName = temp;
        return element.currentStyle[styleName];
    } else {
        return getComputedStyle(element, null).getPropertyValue(styleName);
    }
}
function showsize()
{
    var tag, n;
    // or you can use var allElem=document.all; and loop on it
    for(i = 0; i < document.all.length; i++)
    {    
        tag = document.all(i);
        n = tag.tagName;
        if (n == 'BODY' || n == 'DIV' || n == 'SPAN' || n == 'H1' || n == 'H2' || n == 'H3' || n == 'H4' || n == 'H5' || n == 'H6' || n == 'LI' || n == 'OL' || n == 'UL' || n == 'A'){
            tag.innerHTML = '[' + n + '-' + elementCurrentStyle(tag, 'font-size') + '/' + elementCurrentStyle(tag, 'line-height') + 
            //'/' + elementCurrentStyle(tag, 'color') + 
            ']' + tag.innerHTML;
        }
    }
}
showsize();
