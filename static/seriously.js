var cp437 = (function(){ var d = "\u0000\u0001\u0002\u0003\u0004\u0005\u0006\u0007\b\t\n\u000b\f\r\u000e\u000f\u0010\u0011\u0012\u0013\u0014\u0015\u0016\u0017\u0018\u0019\u001a\u001b\u001c\u001d\u001e\u001f !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~ÇüéâäàåçêëèïîìÄÅÉæÆôöòûùÿÖÜ¢£¥₧ƒáíóúñÑªº¿⌐¬½¼¡«»░▒▓│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀αßΓπΣσµτΦΘΩδ∞φε∩≡±≥≤⌠⌡÷≈°∙·√ⁿ²■ ", D = [], e = {}; for(var i=0;i!=d.length;++i) { if(d.charCodeAt(i) !== 0xFFFD) e[d[i]] = i; D[i] = d.charAt(i); } return {"enc": e, "dec": D }; })();

function genChar() {
	var code = prompt("Generate CP437 Character:");
	$('#code').val($('#code').val() + cp437.dec[parseInt(code)]);
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

function t(s){for(var i=0;i<s.length;i++){console.log(s.charCodeAt(i));}}

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
        }
        if(codeBlock || string || listBlock || numBlock) {
            continue;
        }
        explain += explanations[cp437.enc[c]] +'\r\n';
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
						var code = $.param({
							code : $('#code').val(),
							input : $('#input').val()
						});
						prompt("Permalink:", "http://"
								+ window.location.hostname + "/link/" + code);
						window.location.pathname = "/link/" + code;
					});
			$('#code').on('input propertychange paste', function() {
				updateUtils();
			});
		});