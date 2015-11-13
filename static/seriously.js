var cp437 = {};

cp437.codepage = "\u0000\u0001\u0002\u0003\u0004\u0005\u0006\u0007\b\t\n\u000b\f\r\u000e\u000f\u0010\u0011\u0012\u0013\u0014\u0015\u0016\u0017\u0018\u0019\u001a\u001b\u001c\u001d\u001e\u001f !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~ÇüéâäàåçêëèïîìÄÅÉæÆôöòûùÿÖÜ¢£¥₧ƒáíóúñÑªº¿⌐¬½¼¡«»░▒▓│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀αßΓπΣσµτΦΘΩδ∞φε∩≡±≥≤⌠⌡÷≈°∙·√ⁿ²■ "

cp437.encode = function(codePoint) {
    return cp437.codepage.charAt(codePoint);
}

cp437.decode = function(c) {
    return cp437.codepage.indexOf(c);
}

function genChar() {
	var code = prompt("Generate CP437 Character:");
    if(!code)
        return;
	$('#code').val($('#code').val() + cp437.encode(parseInt(code)));
	updateByteCount();
};

function getByteCount(s) {
    var count = 0, stringLength = s.length;
    s = String(s || "");
    for (var i = 0; i < stringLength; i++) {
        var partCount = encodeURI(s[i]).split("%").length;
        count += partCount == 1 ? 1 : partCount - 1;
    }
    return count;
}

function updateByteCount() {
	var c = $('#code').val();
	var byteCount = c.length;
	var charCount = c.length;
	var s = byteCount + " bytes and " + charCount + " chars long.";
	$('#byteCount').html(s);
}

function getExplanation() {
    var string = false;
    var codeBlock = false;
    var listBlock = false;
    var numBlock = false;
    var code = $('#code').val();
    var explain = '';
    for(var x=0; x < code.length; x++) {
        var c = code.charAt(x);
        if(c === '"') {
            if(string) {
                var prev = code.lastIndexOf('"',x-1);
                var strval = code.slice(prev+1,x);
                explain += 'push the string value "'+strval+'"\r\n'
            }
            string = !string;
            continue;
        } else if(c === '`') {
            if(codeBlock) {
                var prev = code.lastIndexOf('`',x-1);
                var strval = code.slice(prev+1,x);
                explain += 'push the function value `'+strval+'`\r\n'
            }
            codeBlock = !codeBlock;
            continue;
        } else if(c === '[') {
            listBlock = true;
            continue;
        } else if(c === ':') {
            if(numBlock) {
                var prev = code.lastIndexOf(':',x-1);
                var strval = code.slice(prev+1,x);
                explain += 'push the numeric value "'+strval+'"\r\n'
            }
            numBlock = !numBlock;
            continue;
        } else if(c === ']') {
            listBlock = false;
            var prev = code.lastIndexOf('[',x-1);
            var strval = code.slice(prev+1,x);
            explain += 'push the list value "'+strval+'"\r\n'
            continue;
        }
        if(codeBlock || string || listBlock || numBlock) {
            continue;
        }
        if(cp437.decode(c) > -1)
            explain += explanations[cp437.decode(c)] +'\r\n';
    }
    if(string) {
        var prev = code.lastIndexOf('"',x-1);
        var strval = code.slice(prev+1,x);
        explain += 'push the string value "'+strval+'"\r\n'
    } else if(codeBlock) {
        var prev = code.lastIndexOf('"',x-1);
        var strval = code.slice(prev+1,x);
        explain += 'push the function value `'+strval+'`\r\n'
    } else if(listBlock) {
        var prev = code.lastIndexOf('[',x-1);
        var strval = code.slice(prev+1,x);
        explain += 'push the list value "'+strval+'"\r\n'
    } else if(numBlock) {
        var prev = code.lastIndexOf(':',x-1);
        var strval = code.slice(prev+1,x);
        explain += 'push the numeric value "'+strval+'"\r\n'
    }
    $('#explanation').html(explain);
}

function updateUtils() {
	updateByteCount();
	getExplanation();
}

updateUtils();

$(document).ready(
		function() {
			$("#permalink").click(
					function() {
						var code = $('#code').val();
						var	input = $('#input').val();
						prompt("Permalink:", "http://"
								+ window.location.hostname + "/link/" + code + "/" + input);
						window.location.pathname = "/link/" + code + "/" + input;
					});
			$('#code').on('input propertychange paste', function() {
				updateUtils();
			});
            $("input").keypress(function(e){
                var charCode = !e.charCode ? e.which : e.charCode;
                var c = String.fromCharCode(charCode);
                if(cp437.decode(c) < 0)
                    e.preventDefault();
            });
		});