$((function(){$(".image-url-generator").each((function(){var i=$(this),d=i.find("form"),e=d.find("select#id_filter_method"),a=d.find("input#id_width"),l=d.find("input#id_height"),r=d.find("input#id_closeness"),o=i.find("#result-url"),n=i.find(".loading-mask"),p=i.find("img.preview"),s=$("#note-size"),t=i.data("generatorUrl");function f(){var i=e.val();n.addClass("loading"),"original"===i?(a.prop("disabled",!0),l.prop("disabled",!0),r.prop("disabled",!0)):"width"===i?(a.prop("disabled",!1),l.prop("disabled",!0),r.prop("disabled",!0),i+="-"+a.val()):"height"===i?(a.prop("disabled",!0),l.prop("disabled",!1),r.prop("disabled",!0),i+="-"+l.val()):"min"!==i&&"max"!==i&&"fill"!==i||(a.prop("disabled",!1),l.prop("disabled",!1),"fill"===i?(r.prop("disabled",!1),i+="-"+a.val()+"x"+l.val()+"-c"+r.val()):(r.prop("disabled",!0),i+="-"+a.val()+"x"+l.val())),a.val()>$(window).width()?s.show():s.hide(),$.getJSON(t.replace("__filterspec__",i)).done((function(i){o.val(i.url),p.attr("src",i.preview_url),n.removeClass("loading")})).fail((function(i){o.val(i.responseJSON.error),p.attr("src",""),n.removeClass("loading")}))}d.on("change",$.debounce(500,f)),d.on("keyup",$.debounce(500,f)),f()}))}));
