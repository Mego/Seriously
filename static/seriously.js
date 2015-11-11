function genChar() {
    var cp437 = (function(){ var d = "\u0000\u0001\u0002\u0003\u0004\u0005\u0006\u0007\b\t\n\u000b\f\r\u000e\u000f\u0010\u0011\u0012\u0013\u0014\u0015\u0016\u0017\u0018\u0019\u001a\u001b\u001c\u001d\u001e\u001f !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~ÇüéâäàåçêëèïîìÄÅÉæÆôöòûùÿÖÜ¢£¥₧ƒáíóúñÑªº¿⌐¬½¼¡«»░▒▓│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀αßΓπΣσµτΦΘΩδ∞φε∩≡±≥≤⌠⌡÷≈°∙·√ⁿ²■ ", D = [], e = {}; for(var i=0;i!=d.length;++i) { if(d.charCodeAt(i) !== 0xFFFD) e[d[i]] = i; D[i] = d.charAt(i); } return {"enc": e, "dec": D }; })();
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

function getStrippedCode() {
	var stripped = $('#code').val();
	$('#stripped').html(
			'Stripped code: <code>' + stripped + '</code> Byte count: '
					+ getByteCount(stripped));
}

var string = false;
var codeBlock = false;

function getExplanation() {
	$('#explanation').html("This doesn't work right now.");
}

function updateUtils() {
	updateByteCount();
	getStrippedCode();
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