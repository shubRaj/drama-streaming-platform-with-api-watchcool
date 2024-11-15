! function(e) {
    "use strict";
    if (e("body").on("click", ".btn-service", function(t) {
            var a = e(this).attr("data-embed"),
                n = e(this).find(".name").text();
            e(".btn-service").removeClass("selected"), e(this).addClass("selected"), e(".embed-play .play-btn").attr("data-embed", a), e(".embed-play").removeClass("d-none"), e(".embed-code").addClass("d-none"), n && e("a.dropdown-toggle.btn-service span").text(n), e(".embed-code").html("")
        }), e("body").on("click", ".embed-play .play-btn", function(t) {
            var a = e(this).attr("data-embed"),
                n = e(this).attr("_token"),
                t = e(this).attr("type");
            e(".embed-play").addClass("d-none"), e(".embed-code").removeClass("d-none"), e(".spinner").removeClass("d-none"), e.ajax({
                url: _URL + "/ajax/embed/",
                type: "POST",
                headers: {
                    "X-CSRFToken": n
                },
                data: {
                    id: a,
                    type:t,
                },
                success: function(t) {
                    e(".embed-code").html(t), e(".spinner").addClass("d-none"), e("#player").removeClass("d-none"), new Plyr(document.getElementById("player")).on("ready", function(e) {
                        var t, a = e.detail.plyr,
                            n = null,
                            s = a.media.querySelectorAll("source");
                        for (t = 0; t < s.length; ++t)(s[t].src.indexOf(".m3u8") > -1 || s[t].src.indexOf(".txt") > -1 || s[t].src.indexOf(".ts") > -1) && (n = s[t].src);
                        if (null !== n && Hls.isSupported()) {
                            var o = new Hls;
                            o.loadSource(n), o.attachMedia(a.media), o.on(Hls.Events.MANIFEST_PARSED, function() {
                                console.log("MANIFEST_PARSED")
                            })
                        }
                    })
                }
            })
        }), e(".btn-service.selected").trigger("click"), e(document).on("click", "button.btn-follow", function(t) {
            if (!_Auth) return Snackbar.show({
                text: __("You must sign in"),
                customClass: "bg-danger"
            }), !1;
            t.preventDefault();
            var a = e(this),
                n = e(this).attr("data-id");
            a.hasClass("active") ? (e.ajax({
                url: _URL + "/ajax/follow",
                type: "POST",
                dataType: "json",
                data: {
                    content_id: n
                }
            }), a.removeClass("active"), a.text(__("Follow"))) : (e.ajax({
                url: _URL + "/ajax/follow",
                type: "POST",
                dataType: "json",
                data: {
                    content_id: n
                }
            }), a.addClass("active"), a.text(__("Following")))
        }), e("body").on("change", '.collections input[name="collection"]', function(t) {
            var a = e('[name="post_id"]').val(),
                n = e(this).val();
            return e.ajax({
                url: _URL + "/ajax/savecollection",
                type: "POST",
                dataType: "json",
                data: {
                    content_id: a,
                    collection_id: n
                },
                success: function(t) {
                    e(".modal").modal("hide"), Snackbar.show({
                        text: t.text,
                        customClass: "bg-" + t.status
                    })
                }
            }), !1
        }), e(".action-btns .action-btn").on("click", function(t) {
            var a = e(this).attr("data-id");
            if (!_Auth) return Snackbar.show({
                text: __("You must sign in"),
                customClass: "bg-danger"
            }), !1;
            t.preventDefault();
            var n, s = e(t.currentTarget),
                o = s.parent(),
                d = o.find(".like"),
                l = o.find(".dislike"),
                i = o.find(".like span"),
                c = o.find(".dislike span"),
                r = parseInt(i.data("votes")),
                m = parseInt(c.data("votes")),
                u = function(e) {
                    i.data("votes", e).text(e || "0")
                },
                v = function(e) {
                    c.data("votes", e).text(e || "0")
                };
            s.hasClass("like") ? s.hasClass("active") ? (s.removeClass("active"), u(r - 1), n = "-up") : (n = "up", l.hasClass("active") && (l.removeClass("active"), v(m - 1)), s.addClass("active"), u(r + 1)) : s.hasClass("active") ? (s.removeClass("active"), v(m - 1), n = "-down") : (n = "down", d.hasClass("active") && (d.removeClass("active"), u(r - 1)), s.addClass("active"), v(m + 1)), e.ajax({
                url: _URL + "/ajax/reaction",
                type: "post",
                data: {
                    type: n,
                    id: a
                }
            })
        }), e(".comments").length > 0) {
        var t = e(".comments").attr("data-content"),
            a = e(".comments").attr("data-type");
        new Comments(e(".comments"), {
            ajaxUrl: _URL + "/comments",
            content: t,
            type: a,
            sortBy: 1,
            replies: !0,
            maxDepth: 1
        })
    }
}(jQuery);