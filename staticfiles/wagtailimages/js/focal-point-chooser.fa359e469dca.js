var jcropapi;function setupJcrop(t,i,o,e){t.Jcrop({trueSize:[i.width,i.height],bgColor:"rgb(192, 192, 192)",onSelect:function(t){var i=Math.floor((t.x+t.x2)/2),o=Math.floor((t.y+t.y2)/2),a=Math.floor(t.w),h=Math.floor(t.h);e.x.val(i),e.y.val(o),e.width.val(a),e.height.val(h)},onRelease:function(){e.x.val(o.x),e.y.val(o.y),e.width.val(o.width),e.height.val(o.height)}},(function(){$("img",this.ui.holder).attr("alt","");const t=o.label;if(!t)return;const i="jcrop-holder-input";$("input",this.ui.holder).attr("id",i);const e=document.createElement("label");e.setAttribute("for",i),e.classList.add("visuallyhidden"),e.textContent=t,document.getElementsByClassName("jcrop-holder")[0].prepend(e)}))}$((function(){var t=$("div.focal-point-chooser"),i=$(".current-focal-point-indicator",t),o=$("img",t),e={width:o.data("originalWidth"),height:o.data("originalHeight")},a={label:t.data("focalInputLabel"),x:t.data("focalPointX"),y:t.data("focalPointY"),width:t.data("focalPointWidth"),height:t.data("focalPointHeight")},h={x:$("input.focal_point_x"),y:$("input.focal_point_y"),width:$("input.focal_point_width"),height:$("input.focal_point_height")},l=a.x-a.width/2,n=a.y-a.height/2,r=a.width,c=a.height;i.css("left",100*l/e.width+"%"),i.css("top",100*n/e.height+"%"),i.css("width",100*r/e.width+"%"),i.css("height",100*c/e.height+"%");var d=[o,e,a,h];setupJcrop.apply(this,d),$(window).on("resize",$.debounce(300,(function(){jcropapi.destroy(),o.removeAttr("style"),$(".jcrop-holder").remove(),setupJcrop.apply(this,d)}))),$(".remove-focal-point").on("click",(function(){jcropapi.destroy(),o.removeAttr("style"),$(".jcrop-holder").remove(),$(".current-focal-point-indicator").remove(),h.x.val(""),h.y.val(""),h.width.val(""),h.height.val(""),setupJcrop.apply(this,d)}))}));
