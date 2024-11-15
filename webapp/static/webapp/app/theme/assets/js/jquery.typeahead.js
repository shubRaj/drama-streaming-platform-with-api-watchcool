/*!
 * jQuery Typeahead
 * Copyright (C) 2019 RunningCoder.org
 * Licensed under the MIT license
 *
 * @author Tom Bertrand
 * @version 2.11.0 (2019-10-31)
 * @link http://www.runningcoder.org/jquerytypeahead/
 */
var t;
t = function(t) {
    window.Typeahead = {
        version: "2.11.0"
    };
    var e, i = {
            input: null,
            minLength: 2,
            maxLength: !1,
            maxItem: 8,
            dynamic: !1,
            delay: 300,
            order: null,
            offset: !1,
            hint: !1,
            accent: !1,
            highlight: !0,
            multiselect: null,
            group: !1,
            groupOrder: null,
            maxItemPerGroup: null,
            dropdownFilter: !1,
            dynamicFilter: null,
            backdrop: !1,
            backdropOnFocus: !1,
            cache: !1,
            ttl: 36e5,
            compression: !1,
            searchOnFocus: !1,
            blurOnTab: !0,
            resultContainer: null,
            generateOnLoad: null,
            mustSelectItem: !1,
            href: null,
            display: ["display"],
            template: null,
            templateValue: null,
            groupTemplate: null,
            correlativeTemplate: !1,
            emptyTemplate: !1,
            cancelButton: !0,
            loadingAnimation: !0,
            asyncResult: !1,
            filter: !0,
            matcher: null,
            source: null,
            callback: {
                onInit: null,
                onReady: null,
                onShowLayout: null,
                onHideLayout: null,
                onSearch: null,
                onResult: null,
                onLayoutBuiltBefore: null,
                onLayoutBuiltAfter: null,
                onNavigateBefore: null,
                onNavigateAfter: null,
                onEnter: null,
                onLeave: null,
                onClickBefore: null,
                onClickAfter: null,
                onDropdownFilter: null,
                onSendRequest: null,
                onReceiveRequest: null,
                onPopulateSource: null,
                onCacheSave: null,
                onSubmit: null,
                onCancel: null
            },
            selector: {
                container: "typeahead__container",
                result: "typeahead__result",
                list: "typeahead__list",
                group: "typeahead__group",
                item: "typeahead__item",
                empty: "typeahead__empty",
                display: "typeahead__display",
                query: "typeahead__query",
                filter: "typeahead__filter",
                filterButton: "typeahead__filter-button",
                dropdown: "typeahead__dropdown",
                dropdownItem: "typeahead__dropdown-item",
                labelContainer: "typeahead__label-container",
                label: "typeahead__label",
                button: "typeahead__button",
                backdrop: "typeahead__backdrop",
                hint: "typeahead__hint",
                cancelButton: "typeahead__cancel-button"
            },
            debug: !1
        },
        s = {
            from: "Ã£Ã Ã¡Ã¤Ã¢áº½Ã¨Ã©Ã«ÃªÃ¬Ã­Ã¯Ã®ÃµÃ²Ã³Ã¶Ã´Ã¹ÃºÃ¼Ã»Ã±Ã§",
            to: "aaaaaeeeeeiiiiooooouuuunc"
        },
        o = ~window.navigator.appVersion.indexOf("MSIE 9."),
        n = ~window.navigator.appVersion.indexOf("MSIE 10"),
        r = !!~window.navigator.userAgent.indexOf("Trident") && ~window.navigator.userAgent.indexOf("rv:11"),
        a = function(t, e) {
            this.rawQuery = t.val() || "", this.query = t.val() || "", this.selector = t[0].selector, this.deferred = null, this.tmpSource = {}, this.source = {}, this.dynamicGroups = [], this.hasDynamicGroups = !1, this.generatedGroupCount = 0, this.groupBy = "group", this.groups = [], this.searchGroups = [], this.generateGroups = [], this.requestGroups = [], this.result = [], this.tmpResult = {}, this.groupTemplate = "", this.resultHtml = null, this.resultCount = 0, this.resultCountPerGroup = {}, this.options = e, this.node = t, this.namespace = "." + this.helper.slugify.call(this, this.selector) + ".typeahead", this.isContentEditable = void 0 !== this.node.attr("contenteditable") && "false" !== this.node.attr("contenteditable"), this.container = null, this.resultContainer = null, this.item = null, this.items = null, this.comparedItems = null, this.xhr = {}, this.hintIndex = null, this.filters = {
                dropdown: {},
                dynamic: {}
            }, this.dropdownFilter = {
                static: [],
                dynamic: []
            }, this.dropdownFilterAll = null, this.isDropdownEvent = !1, this.requests = {}, this.backdrop = {}, this.hint = {}, this.label = {}, this.hasDragged = !1, this.focusOnly = !1, this.displayEmptyTemplate, this.__construct()
        };
    a.prototype = {
        _validateCacheMethod: function(t) {
            var e;
            if (!0 === t) t = "localStorage";
            else if ("string" == typeof t && !~["localStorage", "sessionStorage"].indexOf(t)) return this.options.debug && (h.log({
                node: this.selector,
                function: "extendOptions()",
                message: 'Invalid options.cache, possible options are "localStorage" or "sessionStorage"'
            }), h.print()), !1;
            e = void 0 !== window[t];
            try {
                window[t].setItem("typeahead", "typeahead"), window[t].removeItem("typeahead")
            } catch (t) {
                e = !1
            }
            return e && t || !1
        },
        extendOptions: function() {
            if (this.options.cache = this._validateCacheMethod(this.options.cache), this.options.compression && ("object" == typeof LZString && this.options.cache || (this.options.debug && (h.log({
                    node: this.selector,
                    function: "extendOptions()",
                    message: "Missing LZString Library or options.cache, no compression will occur."
                }), h.print()), this.options.compression = !1)), this.options.maxLength && !isNaN(this.options.maxLength) || (this.options.maxLength = 1 / 0), void 0 !== this.options.maxItem && ~[0, !1].indexOf(this.options.maxItem) && (this.options.maxItem = 1 / 0), this.options.maxItemPerGroup && !/^\d+$/.test(this.options.maxItemPerGroup) && (this.options.maxItemPerGroup = null), this.options.display && !Array.isArray(this.options.display) && (this.options.display = [this.options.display]), this.options.multiselect && (this.items = [], this.comparedItems = [], "string" == typeof this.options.multiselect.matchOn && (this.options.multiselect.matchOn = [this.options.multiselect.matchOn])), this.options.group && (Array.isArray(this.options.group) ? this.options.debug && (h.log({
                    node: this.selector,
                    function: "extendOptions()",
                    message: "options.group must be a boolean|string|object as of 2.5.0"
                }), h.print()) : ("string" == typeof this.options.group ? this.options.group = {
                    key: this.options.group
                } : "boolean" == typeof this.options.group && (this.options.group = {
                    key: "group"
                }), this.options.group.key = this.options.group.key || "group")), this.options.highlight && !~["any", !0].indexOf(this.options.highlight) && (this.options.highlight = !1), this.options.dropdownFilter && this.options.dropdownFilter instanceof Object) {
                Array.isArray(this.options.dropdownFilter) || (this.options.dropdownFilter = [this.options.dropdownFilter]);
                for (var e = 0, o = this.options.dropdownFilter.length; e < o; ++e) this.dropdownFilter[this.options.dropdownFilter[e].value ? "static" : "dynamic"].push(this.options.dropdownFilter[e])
            }
            this.options.dynamicFilter && !Array.isArray(this.options.dynamicFilter) && (this.options.dynamicFilter = [this.options.dynamicFilter]), this.options.accent && ("object" == typeof this.options.accent ? this.options.accent.from && this.options.accent.to && this.options.accent.from.length !== this.options.accent.to.length && this.options.debug && (h.log({
                node: this.selector,
                function: "extendOptions()",
                message: 'Invalid "options.accent", from and to must be defined and same length.'
            }), h.print()) : this.options.accent = s), this.options.groupTemplate && (this.groupTemplate = this.options.groupTemplate), this.options.resultContainer && ("string" == typeof this.options.resultContainer && (this.options.resultContainer = t(this.options.resultContainer)), this.options.resultContainer instanceof t && this.options.resultContainer[0] ? this.resultContainer = this.options.resultContainer : this.options.debug && (h.log({
                node: this.selector,
                function: "extendOptions()",
                message: 'Invalid jQuery selector or jQuery Object for "options.resultContainer".'
            }), h.print())), this.options.group && this.options.group.key && (this.groupBy = this.options.group.key), this.options.callback && this.options.callback.onClick && (this.options.callback.onClickBefore = this.options.callback.onClick, delete this.options.callback.onClick), this.options.callback && this.options.callback.onNavigate && (this.options.callback.onNavigateBefore = this.options.callback.onNavigate, delete this.options.callback.onNavigate), this.options = t.extend(!0, {}, i, this.options)
        },
        unifySourceFormat: function() {
            var t, e, i;
            for (t in this.dynamicGroups = [], Array.isArray(this.options.source) && (this.options.source = {
                    group: {
                        data: this.options.source
                    }
                }), "string" == typeof this.options.source && (this.options.source = {
                    group: {
                        ajax: {
                            url: this.options.source
                        }
                    }
                }), this.options.source.ajax && (this.options.source = {
                    group: {
                        ajax: this.options.source.ajax
                    }
                }), (this.options.source.url || this.options.source.data) && (this.options.source = {
                    group: this.options.source
                }), this.options.source)
                if (this.options.source.hasOwnProperty(t)) {
                    if ("string" == typeof(e = this.options.source[t]) && (e = {
                            ajax: {
                                url: e
                            }
                        }), i = e.url || e.ajax, Array.isArray(i) ? (e.ajax = "string" == typeof i[0] ? {
                            url: i[0]
                        } : i[0], e.ajax.path = e.ajax.path || i[1] || null, delete e.url) : ("object" == typeof e.url ? e.ajax = e.url : "string" == typeof e.url && (e.ajax = {
                            url: e.url
                        }), delete e.url), !e.data && !e.ajax) return this.options.debug && (h.log({
                        node: this.selector,
                        function: "unifySourceFormat()",
                        arguments: JSON.stringify(this.options.source),
                        message: 'Undefined "options.source.' + t + '.[data|ajax]" is Missing - Typeahead dropped'
                    }), h.print()), !1;
                    e.display && !Array.isArray(e.display) && (e.display = [e.display]), e.minLength = "number" == typeof e.minLength ? e.minLength : this.options.minLength, e.maxLength = "number" == typeof e.maxLength ? e.maxLength : this.options.maxLength, e.dynamic = "boolean" == typeof e.dynamic || this.options.dynamic, e.minLength > e.maxLength && (e.minLength = e.maxLength), this.options.source[t] = e, this.options.source[t].dynamic && this.dynamicGroups.push(t), e.cache = void 0 !== e.cache ? this._validateCacheMethod(e.cache) : this.options.cache, e.compression && ("object" == typeof LZString && e.cache || (this.options.debug && (h.log({
                        node: this.selector,
                        function: "unifySourceFormat()",
                        message: "Missing LZString Library or group.cache, no compression will occur on group: " + t
                    }), h.print()), e.compression = !1))
                } return this.hasDynamicGroups = this.options.dynamic || !!this.dynamicGroups.length, !0
        },
        init: function() {
            this.helper.executeCallback.call(this, this.options.callback.onInit, [this.node]), this.container = this.node.closest("." + this.options.selector.container), this.options.debug && (h.log({
                node: this.selector,
                function: "init()",
                message: "OK - Typeahead activated on " + this.selector
            }), h.print())
        },
        delegateEvents: function() {
            var e = this,
                i = ["focus" + this.namespace, "input" + this.namespace, "propertychange" + this.namespace, "keydown" + this.namespace, "keyup" + this.namespace, "search" + this.namespace, "generate" + this.namespace];
            t("html").on("touchmove", (function() {
                e.hasDragged = !0
            })).on("touchstart", (function() {
                e.hasDragged = !1
            })), this.node.closest("form").on("submit", (function(t) {
                if (!e.options.mustSelectItem || !e.helper.isEmpty(e.item)) return e.options.backdropOnFocus || e.hideLayout(), e.options.callback.onSubmit ? e.helper.executeCallback.call(e, e.options.callback.onSubmit, [e.node, this, e.item || e.items, t]) : void 0;
                t.preventDefault()
            })).on("reset", (function() {
                setTimeout((function() {
                    e.node.trigger("input" + e.namespace), e.hideLayout()
                }))
            }));
            var s = !1;
            if (this.node.attr("placeholder") && (n || r)) {
                var a = !0;
                this.node.on("focusin focusout", (function() {
                    a = !(this.value || !this.placeholder)
                })), this.node.on("input", (function(t) {
                    a && (t.stopImmediatePropagation(), a = !1)
                }))
            }
            this.node.off(this.namespace).on(i.join(" "), (function(i, n) {
                switch (i.type) {
                    case "generate":
                        e.generateSource(Object.keys(e.options.source));
                        break;
                    case "focus":
                        if (e.focusOnly) {
                            e.focusOnly = !1;
                            break
                        }
                        e.options.backdropOnFocus && (e.buildBackdropLayout(), e.showLayout()), e.options.searchOnFocus && !e.item && (e.deferred = t.Deferred(), e.assignQuery(), e.generateSource());
                        break;
                    case "keydown":
                        8 === i.keyCode && e.options.multiselect && e.options.multiselect.cancelOnBackspace && "" === e.query && e.items.length ? e.cancelMultiselectItem(e.items.length - 1, null, i) : i.keyCode && ~[9, 13, 27, 38, 39, 40].indexOf(i.keyCode) && (s = !0, e.navigate(i));
                        break;
                    case "keyup":
                        o && e.node[0].value.replace(/^\s+/, "").toString().length < e.query.length && e.node.trigger("input" + e.namespace);
                        break;
                    case "propertychange":
                        if (s) {
                            s = !1;
                            break
                        }
                        case "input":
                            e.deferred = t.Deferred(), e.assignQuery(), "" === e.rawQuery && "" === e.query && (i.originalEvent = n || {}, e.helper.executeCallback.call(e, e.options.callback.onCancel, [e.node, e.item, i]), e.item = null), e.options.cancelButton && e.toggleCancelButtonVisibility(), e.options.hint && e.hint.container && "" !== e.hint.container.val() && 0 !== e.hint.container.val().indexOf(e.rawQuery) && (e.hint.container.val(""), e.isContentEditable && e.hint.container.text("")), e.hasDynamicGroups ? e.helper.typeWatch((function() {
                                e.generateSource()
                            }), e.options.delay) : e.generateSource();
                            break;
                        case "search":
                            e.searchResult(), e.buildLayout(), e.result.length || e.searchGroups.length && e.displayEmptyTemplate ? e.showLayout() : e.hideLayout(), e.deferred && e.deferred.resolve()
                }
                return e.deferred && e.deferred.promise()
            })), this.options.generateOnLoad && this.node.trigger("generate" + this.namespace)
        },
        assignQuery: function() {
            this.isContentEditable ? this.rawQuery = this.node.text() : this.rawQuery = this.node.val().toString(), this.rawQuery = this.rawQuery.replace(/^\s+/, ""), this.rawQuery !== this.query && (this.query = this.rawQuery)
        },
        filterGenerateSource: function() {
            if (this.searchGroups = [], this.generateGroups = [], !this.focusOnly || this.options.multiselect)
                for (var t in this.options.source)
                    if (this.options.source.hasOwnProperty(t) && this.query.length >= this.options.source[t].minLength && this.query.length <= this.options.source[t].maxLength) {
                        if (this.filters.dropdown && "group" === this.filters.dropdown.key && this.filters.dropdown.value !== t) continue;
                        if (this.searchGroups.push(t), !this.options.source[t].dynamic && this.source[t]) continue;
                        this.generateGroups.push(t)
                    }
        },
        generateSource: function(e) {
            if (this.filterGenerateSource(), this.generatedGroupCount = 0, Array.isArray(e) && e.length) this.generateGroups = e;
            else if (!this.generateGroups.length) return void this.node.trigger("search" + this.namespace);
            if (this.requestGroups = [], this.options.loadingAnimation && this.container.addClass("loading"), !this.helper.isEmpty(this.xhr)) {
                for (var i in this.xhr) this.xhr.hasOwnProperty(i) && this.xhr[i].abort();
                this.xhr = {}
            }
            for (var s, o, n, r, a, l, c, p = this, u = (i = 0, this.generateGroups.length); i < u; ++i) {
                if (s = this.generateGroups[i], r = (n = this.options.source[s]).cache, a = n.compression, this.options.asyncResult && delete this.source[s], r && (l = window[r].getItem("TYPEAHEAD_" + this.selector + ":" + s))) {
                    a && (l = LZString.decompressFromUTF16(l)), c = !1;
                    try {
                        (l = JSON.parse(l + "")).data && l.ttl > (new Date).getTime() ? (this.populateSource(l.data, s), c = !0, this.options.debug && (h.log({
                            node: this.selector,
                            function: "generateSource()",
                            message: 'Source for group "' + s + '" found in ' + r
                        }), h.print())) : window[r].removeItem("TYPEAHEAD_" + this.selector + ":" + s)
                    } catch (t) {}
                    if (c) continue
                }!n.data || n.ajax ? n.ajax && (this.requests[s] || (this.requests[s] = this.generateRequestObject(s)), this.requestGroups.push(s)) : "function" == typeof n.data ? (o = n.data.call(this), Array.isArray(o) ? p.populateSource(o, s) : "function" == typeof o.promise && function(e) {
                    t.when(o).then((function(t) {
                        t && Array.isArray(t) && p.populateSource(t, e)
                    }))
                }(s)) : this.populateSource(t.extend(!0, [], n.data), s)
            }
            return this.requestGroups.length && this.handleRequests(), this.options.asyncResult && this.searchGroups.length !== this.generateGroups && this.node.trigger("search" + this.namespace), !!this.generateGroups.length
        },
        generateRequestObject: function(t) {
            var e = this,
                i = this.options.source[t],
                s = {
                    request: {
                        url: i.ajax.url || null,
                        dataType: "json",
                        beforeSend: function(s, o) {
                            e.xhr[t] = s;
                            var n = e.requests[t].callback.beforeSend || i.ajax.beforeSend;
                            "function" == typeof n && n.apply(null, arguments)
                        }
                    },
                    callback: {
                        beforeSend: null,
                        done: null,
                        fail: null,
                        then: null,
                        always: null
                    },
                    extra: {
                        path: i.ajax.path || null,
                        group: t
                    },
                    validForGroup: [t]
                };
            if ("function" != typeof i.ajax && (i.ajax instanceof Object && (s = this.extendXhrObject(s, i.ajax)), Object.keys(this.options.source).length > 1))
                for (var o in this.requests) this.requests.hasOwnProperty(o) && (this.requests[o].isDuplicated || s.request.url && s.request.url === this.requests[o].request.url && (this.requests[o].validForGroup.push(t), s.isDuplicated = !0, delete s.validForGroup));
            return s
        },
        extendXhrObject: function(e, i) {
            return "object" == typeof i.callback && (e.callback = i.callback, delete i.callback), "function" == typeof i.beforeSend && (e.callback.beforeSend = i.beforeSend, delete i.beforeSend), e.request = t.extend(!0, e.request, i), "jsonp" !== e.request.dataType.toLowerCase() || e.request.jsonpCallback || (e.request.jsonpCallback = "callback_" + e.extra.group), e
        },
        handleRequests: function() {
            var e, i = this,
                s = this.requestGroups.length;
            if (!1 !== this.helper.executeCallback.call(this, this.options.callback.onSendRequest, [this.node, this.query]))
                for (var o = 0, n = this.requestGroups.length; o < n; ++o) e = this.requestGroups[o], this.requests[e].isDuplicated || function(e, o) {
                    if ("function" == typeof i.options.source[e].ajax) {
                        var n = i.options.source[e].ajax.call(i, i.query);
                        if ("object" != typeof(o = i.extendXhrObject(i.generateRequestObject(e), "object" == typeof n ? n : {})).request || !o.request.url) return i.options.debug && (h.log({
                            node: i.selector,
                            function: "handleRequests",
                            message: 'Source function must return an object containing ".url" key for group "' + e + '"'
                        }), h.print()), void i.populateSource([], e);
                        i.requests[e] = o
                    }
                    var r, a = !1,
                        l = {};
                    if (~o.request.url.indexOf("{{query}}") && (a || (o = t.extend(!0, {}, o), a = !0), o.request.url = o.request.url.replace("{{query}}", encodeURIComponent(i.query))), o.request.data)
                        for (var c in o.request.data)
                            if (o.request.data.hasOwnProperty(c) && ~String(o.request.data[c]).indexOf("{{query}}")) {
                                a || (o = t.extend(!0, {}, o), a = !0), o.request.data[c] = o.request.data[c].replace("{{query}}", i.query);
                                break
                            } t.ajax(o.request).done((function(t, e, s) {
                        for (var n, a = 0, c = o.validForGroup.length; a < c; a++) n = o.validForGroup[a], "function" == typeof(r = i.requests[n]).callback.done && (l[n] = r.callback.done.call(i, t, e, s), Array.isArray(l[n]) && "object" == typeof l[n] || i.options.debug && (h.log({
                            node: i.selector,
                            function: "Ajax.callback.done()",
                            message: "Invalid returned data has to be an Array"
                        }), h.print()))
                    })).fail((function(t, e, s) {
                        for (var n = 0, a = o.validForGroup.length; n < a; n++)(r = i.requests[o.validForGroup[n]]).callback.fail instanceof Function && r.callback.fail.call(i, t, e, s);
                        i.options.debug && (h.log({
                            node: i.selector,
                            function: "Ajax.callback.fail()",
                            arguments: JSON.stringify(o.request),
                            message: e
                        }), console.log(s), h.print())
                    })).always((function(t, e, n) {
                        for (var a, h = 0, c = o.validForGroup.length; h < c; h++) {
                            if (a = o.validForGroup[h], (r = i.requests[a]).callback.always instanceof Function && r.callback.always.call(i, t, e, n), "abort" === e) return;
                            i.populateSource(null !== t && "function" == typeof t.promise && [] || l[a] || t, r.extra.group, r.extra.path || r.request.path), 0 == (s -= 1) && i.helper.executeCallback.call(i, i.options.callback.onReceiveRequest, [i.node, i.query])
                        }
                    })).then((function(t, e) {
                        for (var s = 0, n = o.validForGroup.length; s < n; s++)(r = i.requests[o.validForGroup[s]]).callback.then instanceof Function && r.callback.then.call(i, t, e)
                    }))
                }(e, this.requests[e])
        },
        populateSource: function(e, i, s) {
            var o = this,
                n = this.options.source[i],
                r = n.ajax && n.data;
            s && "string" == typeof s && (e = this.helper.namespace.call(this, s, e)), void 0 === e && this.options.debug && (h.log({
                node: this.selector,
                function: "populateSource()",
                arguments: s,
                message: "Invalid data path."
            }), h.print()), Array.isArray(e) || (this.options.debug && (h.log({
                node: this.selector,
                function: "populateSource()",
                arguments: JSON.stringify({
                    group: i
                }),
                message: "Invalid data type, must be Array type."
            }), h.print()), e = []), r && ("function" == typeof r && (r = r()), Array.isArray(r) ? e = e.concat(r) : this.options.debug && (h.log({
                node: this.selector,
                function: "populateSource()",
                arguments: JSON.stringify(r),
                message: "WARNING - this.options.source." + i + ".data Must be an Array or a function that returns an Array."
            }), h.print()));
            for (var a, l = n.display ? "compiled" === n.display[0] ? n.display[1] : n.display[0] : "compiled" === this.options.display[0] ? this.options.display[1] : this.options.display[0], c = 0, p = e.length; c < p; c++) null !== e[c] && "boolean" != typeof e[c] ? ("string" == typeof e[c] && ((a = {})[l] = e[c], e[c] = a), e[c].group = i) : this.options.debug && (h.log({
                node: this.selector,
                function: "populateSource()",
                message: "WARNING - NULL/BOOLEAN value inside " + i + "! The data was skipped."
            }), h.print());
            if (!this.hasDynamicGroups && this.dropdownFilter.dynamic.length) {
                var u, d, f = {};
                for (c = 0, p = e.length; c < p; c++)
                    for (var g = 0, m = this.dropdownFilter.dynamic.length; g < m; g++) u = this.dropdownFilter.dynamic[g].key, (d = e[c][u]) && (this.dropdownFilter.dynamic[g].value || (this.dropdownFilter.dynamic[g].value = []), f[u] || (f[u] = []), ~f[u].indexOf(d.toLowerCase()) || (f[u].push(d.toLowerCase()), this.dropdownFilter.dynamic[g].value.push(d)))
            }
            if (this.options.correlativeTemplate) {
                var y = n.template || this.options.template,
                    b = "";
                if ("function" == typeof y && (y = y.call(this, "", {})), y) {
                    if (Array.isArray(this.options.correlativeTemplate))
                        for (c = 0, p = this.options.correlativeTemplate.length; c < p; c++) b += "{{" + this.options.correlativeTemplate[c] + "}} ";
                    else b = y.replace(/<.+?>/g, " ").replace(/\s{2,}/, " ").trim();
                    for (c = 0, p = e.length; c < p; c++) e[c].compiled = t("<textarea />").html(b.replace(/\{\{([\w\-\.]+)(?:\|(\w+))?}}/g, (function(t, i) {
                        return o.helper.namespace.call(o, i, e[c], "get", "")
                    })).trim()).text();
                    n.display ? ~n.display.indexOf("compiled") || n.display.unshift("compiled") : ~this.options.display.indexOf("compiled") || this.options.display.unshift("compiled")
                } else this.options.debug && (h.log({
                    node: this.selector,
                    function: "populateSource()",
                    arguments: String(i),
                    message: "WARNING - this.options.correlativeTemplate is enabled but no template was found."
                }), h.print())
            }
            this.options.callback.onPopulateSource && (e = this.helper.executeCallback.call(this, this.options.callback.onPopulateSource, [this.node, e, i, s]), this.options.debug && (e && Array.isArray(e) || (h.log({
                node: this.selector,
                function: "callback.populateSource()",
                message: 'callback.onPopulateSource must return the "data" parameter'
            }), h.print()))), this.tmpSource[i] = Array.isArray(e) && e || [];
            var v = this.options.source[i].cache,
                k = this.options.source[i].compression,
                x = this.options.source[i].ttl || this.options.ttl;
            if (v && !window[v].getItem("TYPEAHEAD_" + this.selector + ":" + i)) {
                this.options.callback.onCacheSave && (e = this.helper.executeCallback.call(this, this.options.callback.onCacheSave, [this.node, e, i, s]), this.options.debug && (e && Array.isArray(e) || (h.log({
                    node: this.selector,
                    function: "callback.populateSource()",
                    message: 'callback.onCacheSave must return the "data" parameter'
                }), h.print())));
                var w = JSON.stringify({
                    data: e,
                    ttl: (new Date).getTime() + x
                });
                k && (w = LZString.compressToUTF16(w)), window[v].setItem("TYPEAHEAD_" + this.selector + ":" + i, w)
            }
            this.incrementGeneratedGroup(i)
        },
        incrementGeneratedGroup: function(t) {
            if (this.generatedGroupCount++, this.generatedGroupCount === this.generateGroups.length || this.options.asyncResult) {
                this.xhr && this.xhr[t] && delete this.xhr[t];
                for (var e = 0, i = this.generateGroups.length; e < i; e++) this.source[this.generateGroups[e]] = this.tmpSource[this.generateGroups[e]];
                this.hasDynamicGroups || this.buildDropdownItemLayout("dynamic"), this.generatedGroupCount === this.generateGroups.length && (this.xhr = {}, this.options.loadingAnimation && this.container.removeClass("loading")), this.node.trigger("search" + this.namespace)
            }
        },
        navigate: function(t) {
            if (this.helper.executeCallback.call(this, this.options.callback.onNavigateBefore, [this.node, this.query, t]), 27 === t.keyCode) return t.preventDefault(), void(this.query.length ? (this.resetInput(), this.node.trigger("input" + this.namespace, [t])) : (this.node.blur(), this.hideLayout()));
            if (this.result.length) {
                var e, i = this.resultContainer.find("." + this.options.selector.item).not("[disabled]"),
                    s = i.filter(".active"),
                    o = s[0] ? i.index(s) : null,
                    n = s[0] ? s.attr("data-index") : null,
                    r = null;
                if (this.clearActiveItem(), this.helper.executeCallback.call(this, this.options.callback.onLeave, [this.node, null !== o && i.eq(o) || void 0, null !== n && this.result[n] || void 0, t]), 13 === t.keyCode) return t.preventDefault(), void(s.length > 0 ? "javascript:;" === s.find("a:first")[0].href ? s.find("a:first").trigger("click", t) : s.find("a:first")[0].click() : this.node.closest("form").trigger("submit"));
                if (39 !== t.keyCode) {
                    9 === t.keyCode ? this.options.blurOnTab ? this.hideLayout() : s.length > 0 ? o + 1 < i.length ? (t.preventDefault(), r = o + 1, this.addActiveItem(i.eq(r))) : this.hideLayout() : i.length ? (t.preventDefault(), r = 0, this.addActiveItem(i.first())) : this.hideLayout() : 38 === t.keyCode ? (t.preventDefault(), s.length > 0 ? o - 1 >= 0 && (r = o - 1, this.addActiveItem(i.eq(r))) : i.length && (r = i.length - 1, this.addActiveItem(i.last()))) : 40 === t.keyCode && (t.preventDefault(), s.length > 0 ? o + 1 < i.length && (r = o + 1, this.addActiveItem(i.eq(r))) : i.length && (r = 0, this.addActiveItem(i.first()))), e = null !== r ? i.eq(r).attr("data-index") : null, this.helper.executeCallback.call(this, this.options.callback.onEnter, [this.node, null !== r && i.eq(r) || void 0, null !== e && this.result[e] || void 0, t]), t.preventInputChange && ~[38, 40].indexOf(t.keyCode) && this.buildHintLayout(null !== e && e < this.result.length ? [this.result[e]] : null), this.options.hint && this.hint.container && this.hint.container.css("color", t.preventInputChange ? this.hint.css.color : null === e && this.hint.css.color || this.hint.container.css("background-color") || "fff");
                    var a = null === e || t.preventInputChange ? this.rawQuery : this.getTemplateValue.call(this, this.result[e]);
                    this.node.val(a), this.isContentEditable && this.node.text(a), this.helper.executeCallback.call(this, this.options.callback.onNavigateAfter, [this.node, i, null !== r && i.eq(r).find("a:first") || void 0, null !== e && this.result[e] || void 0, this.query, t])
                } else null !== o ? i.eq(o).find("a:first")[0].click() : this.options.hint && "" !== this.hint.container.val() && this.helper.getCaret(this.node[0]) >= this.query.length && i.filter('[data-index="' + this.hintIndex + '"]').find("a:first")[0].click()
            }
        },
        getTemplateValue: function(t) {
            if (t) {
                var e = t.group && this.options.source[t.group].templateValue || this.options.templateValue;
                if ("function" == typeof e && (e = e.call(this)), !e) return this.helper.namespace.call(this, t.matchedKey, t).toString();
                var i = this;
                return e.replace(/\{\{([\w\-.]+)}}/gi, (function(e, s) {
                    return i.helper.namespace.call(i, s, t, "get", "")
                }))
            }
        },
        clearActiveItem: function() {
            this.resultContainer.find("." + this.options.selector.item).removeClass("active")
        },
        addActiveItem: function(t) {
            t.addClass("active")
        },
        searchResult: function() {
            this.resetLayout(), !1 !== this.helper.executeCallback.call(this, this.options.callback.onSearch, [this.node, this.query]) && (!this.searchGroups.length || this.options.multiselect && this.options.multiselect.limit && this.items.length >= this.options.multiselect.limit || this.searchResultData(), this.helper.executeCallback.call(this, this.options.callback.onResult, [this.node, this.query, this.result, this.resultCount, this.resultCountPerGroup]), this.isDropdownEvent && (this.helper.executeCallback.call(this, this.options.callback.onDropdownFilter, [this.node, this.query, this.filters.dropdown, this.result]), this.isDropdownEvent = !1))
        },
        searchResultData: function() {
            var e, i, s, o, n, r, a, l, c, p, u, d = this,
                f = this.groupBy,
                g = null,
                m = this.query.toLowerCase(),
                y = this.options.maxItem,
                b = this.options.maxItemPerGroup,
                v = this.filters.dynamic && !this.helper.isEmpty(this.filters.dynamic),
                k = {},
                x = "function" == typeof this.options.matcher && this.options.matcher;
            this.options.accent && (m = this.helper.removeAccent.call(this, m));
            for (var w = 0, C = this.searchGroups.length; w < C; ++w)
                if (G = this.searchGroups[w], (!this.filters.dropdown || "group" !== this.filters.dropdown.key || this.filters.dropdown.value === G) && (n = void 0 !== this.options.source[G].filter ? this.options.source[G].filter : this.options.filter, a = "function" == typeof this.options.source[G].matcher && this.options.source[G].matcher || x, this.source[G]))
                    for (var S = 0, q = this.source[G].length; S < q && (!(this.resultItemCount >= y) || this.options.callback.onResult); S++)
                        if ((!v || this.dynamicFilter.validate.apply(this, [this.source[G][S]])) && null !== (e = this.source[G][S]) && "boolean" != typeof e && (!this.options.multiselect || this.isMultiselectUniqueData(e)) && (!this.filters.dropdown || (e[this.filters.dropdown.key] || "").toLowerCase() === (this.filters.dropdown.value || "").toLowerCase())) {
                            if ((g = "group" === f ? G : e[f] ? e[f] : e.group) && !this.tmpResult[g] && (this.tmpResult[g] = [], this.resultCountPerGroup[g] = 0), b && "group" === f && this.tmpResult[g].length >= b && !this.options.callback.onResult) break;
                            for (var A = 0, O = (I = this.options.source[G].display || this.options.display).length; A < O; ++A) {
                                if (!1 !== n) {
                                    if (void 0 === (o = /\./.test(I[A]) ? this.helper.namespace.call(this, I[A], e) : e[I[A]]) || "" === o) {
                                        this.options.debug && (k[A] = {
                                            display: I[A],
                                            data: e
                                        });
                                        continue
                                    }
                                    o = this.helper.cleanStringFromScript(o)
                                }
                                if ("function" == typeof n) {
                                    if (void 0 === (r = n.call(this, e, o))) break;
                                    if (!r) continue;
                                    "object" == typeof r && (e = r)
                                }
                                if (~[void 0, !0].indexOf(n)) {
                                    if (null === o) continue;
                                    if (s = (s = o).toString().toLowerCase(), this.options.accent && (s = this.helper.removeAccent.call(this, s)), i = s.indexOf(m), this.options.correlativeTemplate && "compiled" === I[A] && i < 0 && /\s/.test(m)) {
                                        c = !0, u = s;
                                        for (var L = 0, F = (p = m.split(" ")).length; L < F; L++)
                                            if ("" !== p[L]) {
                                                if (!~u.indexOf(p[L])) {
                                                    c = !1;
                                                    break
                                                }
                                                u = u.replace(p[L], "")
                                            }
                                    }
                                    if (i < 0 && !c) continue;
                                    if (this.options.offset && 0 !== i) continue;
                                    if (a) {
                                        if (void 0 === (l = a.call(this, e, o))) break;
                                        if (!l) continue;
                                        "object" == typeof l && (e = l)
                                    }
                                }
                                if (this.resultCount++, this.resultCountPerGroup[g]++, this.resultItemCount < y) {
                                    if (b && this.tmpResult[g].length >= b) break;
                                    this.tmpResult[g].push(t.extend(!0, {
                                        matchedKey: I[A]
                                    }, e)), this.resultItemCount++
                                }
                                break
                            }
                            if (!this.options.callback.onResult) {
                                if (this.resultItemCount >= y) break;
                                if (b && this.tmpResult[g].length >= b && "group" === f) break
                            }
                        } if (this.options.debug && (this.helper.isEmpty(k) || (h.log({
                    node: this.selector,
                    function: "searchResult()",
                    arguments: JSON.stringify(k),
                    message: "Missing keys for display, make sure options.display is set properly."
                }), h.print())), this.options.order) {
                var j, I = [];
                for (var G in this.tmpResult)
                    if (this.tmpResult.hasOwnProperty(G)) {
                        for (w = 0, C = this.tmpResult[G].length; w < C; w++) j = this.options.source[this.tmpResult[G][w].group].display || this.options.display, ~I.indexOf(j[0]) || I.push(j[0]);
                        this.tmpResult[G].sort(d.helper.sort(I, "asc" === d.options.order, (function(t) {
                            return t ? t.toString().toUpperCase() : ""
                        })))
                    }
            }
            var T = [],
                R = [];
            for (w = 0, C = (R = "function" == typeof this.options.groupOrder ? this.options.groupOrder.apply(this, [this.node, this.query, this.tmpResult, this.resultCount, this.resultCountPerGroup]) : Array.isArray(this.options.groupOrder) ? this.options.groupOrder : "string" == typeof this.options.groupOrder && ~["asc", "desc"].indexOf(this.options.groupOrder) ? Object.keys(this.tmpResult).sort(d.helper.sort([], "asc" === d.options.groupOrder, (function(t) {
                    return t.toString().toUpperCase()
                }))) : Object.keys(this.tmpResult)).length; w < C; w++) T = T.concat(this.tmpResult[R[w]] || []);
            this.groups = JSON.parse(JSON.stringify(R)), this.result = T
        },
        buildLayout: function() {
            this.buildHtmlLayout(), this.buildBackdropLayout(), this.buildHintLayout(), this.options.callback.onLayoutBuiltBefore && (this.tmpResultHtml = this.helper.executeCallback.call(this, this.options.callback.onLayoutBuiltBefore, [this.node, this.query, this.result, this.resultHtml])), this.tmpResultHtml instanceof t ? this.resultContainer.html(this.tmpResultHtml) : this.resultHtml instanceof t && this.resultContainer.html(this.resultHtml), this.options.callback.onLayoutBuiltAfter && this.helper.executeCallback.call(this, this.options.callback.onLayoutBuiltAfter, [this.node, this.query, this.result])
        },
        buildHtmlLayout: function() {
            if (!1 !== this.options.resultContainer) {
                var e;
                if (this.resultContainer || (this.resultContainer = t("<div/>", {
                        class: this.options.selector.result
                    }), this.container.append(this.resultContainer)), !this.result.length && this.generatedGroupCount === this.generateGroups.length)
                    if (this.options.multiselect && this.options.multiselect.limit && this.items.length >= this.options.multiselect.limit) e = this.options.multiselect.limitTemplate ? "function" == typeof this.options.multiselect.limitTemplate ? this.options.multiselect.limitTemplate.call(this, this.query) : this.options.multiselect.limitTemplate.replace(/\{\{query}}/gi, t("<div>").text(this.helper.cleanStringFromScript(this.query)).html()) : "Can't select more than " + this.items.length + " items.";
                    else {
                        if (!this.options.emptyTemplate || "" === this.query) return;
                        e = "function" == typeof this.options.emptyTemplate ? this.options.emptyTemplate.call(this, this.query) : this.options.emptyTemplate.replace(/\{\{query}}/gi, t("<div>").text(this.helper.cleanStringFromScript(this.query)).html())
                    } this.displayEmptyTemplate = !!e;
                var i = this.query.toLowerCase();
                this.options.accent && (i = this.helper.removeAccent.call(this, i));
                var s = this,
                    o = this.groupTemplate || "<ul></ul>",
                    n = !1;
                this.groupTemplate ? o = t(o.replace(/<([^>]+)>\{\{(.+?)}}<\/[^>]+>/g, (function(t, i, o, r, a) {
                    var l = "",
                        h = "group" === o ? s.groups : [o];
                    if (!s.result.length) return !0 === n ? "" : (n = !0, "<" + i + ' class="' + s.options.selector.empty + '">' + e + "</" + i + ">");
                    for (var c = 0, p = h.length; c < p; ++c) l += "<" + i + ' data-group-template="' + h[c] + '"><ul></ul></' + i + ">";
                    return l
                }))) : (o = t(o), this.result.length || o.append(e instanceof t ? e : '<li class="' + s.options.selector.empty + '">' + e + "</li>")), o.addClass(this.options.selector.list + (this.helper.isEmpty(this.result) ? " empty" : ""));
                for (var r, a, l, h, c, p, u, d, f, g, m, y, b, v = this.groupTemplate && this.result.length && s.groups || [], k = 0, x = this.result.length; k < x; ++k) r = (l = this.result[k]).group, h = !this.options.multiselect && this.options.source[l.group].href || this.options.href, d = [], f = this.options.source[l.group].display || this.options.display, this.options.group && (r = l[this.options.group.key], this.options.group.template && ("function" == typeof this.options.group.template ? a = this.options.group.template.call(this, l) : "string" == typeof this.options.group.template && (a = this.options.group.template.replace(/\{\{([\w\-\.]+)}}/gi, (function(t, e) {
                        return s.helper.namespace.call(s, e, l, "get", "")
                    })))), o.find('[data-search-group="' + r + '"]')[0] || (this.groupTemplate ? o.find('[data-group-template="' + r + '"] ul') : o).append(t("<li/>", {
                        class: s.options.selector.group,
                        html: t("<a/>", {
                            href: "javascript:;",
                            html: a || r,
                            tabindex: -1
                        }),
                        "data-search-group": r
                    }))), this.groupTemplate && v.length && ~(m = v.indexOf(r || l.group)) && v.splice(m, 1), c = t("<li/>", {
                        class: s.options.selector.item + " " + s.options.selector.group + "-" + this.helper.slugify.call(this, r),
                        disabled: !!l.disabled,
                        "data-group": r,
                        "data-index": k,
                        html: t("<a/>", {
                            href: h && !l.disabled ? (y = h, b = l, b.href = s.generateHref.call(s, y, b)) : "javascript:;",
                            html: function() {
                                if (p = l.group && s.options.source[l.group].template || s.options.template) "function" == typeof p && (p = p.call(s, s.query, l)), u = p.replace(/\{\{([^\|}]+)(?:\|([^}]+))*}}/gi, (function(t, e, o) {
                                    var n = s.helper.cleanStringFromScript(String(s.helper.namespace.call(s, e, l, "get", "")));
                                    return ~(o = o && o.split("|") || []).indexOf("slugify") && (n = s.helper.slugify.call(s, n)), ~o.indexOf("raw") || !0 === s.options.highlight && i && ~f.indexOf(e) && (n = s.helper.highlight.call(s, n, i.split(" "), s.options.accent)), n
                                }));
                                else {
                                    for (var e = 0, o = f.length; e < o; e++) void 0 !== (g = /\./.test(f[e]) ? s.helper.namespace.call(s, f[e], l, "get", "") : l[f[e]]) && "" !== g && d.push(g);
                                    u = '<span class="' + s.options.selector.display + '">' + s.helper.cleanStringFromScript(String(d.join(" "))) + "</span>"
                                }(!0 === s.options.highlight && i && !p || "any" === s.options.highlight) && (u = s.helper.highlight.call(s, u, i.split(" "), s.options.accent)), t(this).append(u)
                            }
                        })
                    }),
                    function(e, i, o) {
                        o.on("click", (function(e, o) {
                            i.disabled ? e.preventDefault() : (o && "object" == typeof o && (e.originalEvent = o), s.options.mustSelectItem && s.helper.isEmpty(i) ? e.preventDefault() : (s.options.multiselect || (s.item = i), !1 !== s.helper.executeCallback.call(s, s.options.callback.onClickBefore, [s.node, t(this), i, e]) && (e.originalEvent && e.originalEvent.defaultPrevented || e.isDefaultPrevented() || (s.options.multiselect ? (s.query = s.rawQuery = "", s.addMultiselectItemLayout(i)) : (s.focusOnly = !0, s.query = s.rawQuery = s.getTemplateValue.call(s, i), s.isContentEditable && (s.node.text(s.query), s.helper.setCaretAtEnd(s.node[0]))), s.hideLayout(), s.node.val(s.query).focus(), s.options.cancelButton && s.toggleCancelButtonVisibility(), s.helper.executeCallback.call(s, s.options.callback.onClickAfter, [s.node, t(this), i, e])))))
                        })), o.on("mouseenter", (function(e) {
                            i.disabled || (s.clearActiveItem(), s.addActiveItem(t(this))), s.helper.executeCallback.call(s, s.options.callback.onEnter, [s.node, t(this), i, e])
                        })), o.on("mouseleave", (function(e) {
                            i.disabled || s.clearActiveItem(), s.helper.executeCallback.call(s, s.options.callback.onLeave, [s.node, t(this), i, e])
                        }))
                    }(0, l, c), (this.groupTemplate ? o.find('[data-group-template="' + r + '"] ul') : o).append(c);
                if (this.result.length && v.length)
                    for (k = 0, x = v.length; k < x; ++k) o.find('[data-group-template="' + v[k] + '"]').remove();
                this.resultHtml = o
            }
        },
        generateHref: function(t, e) {
            var i = this;
            return "string" == typeof t ? t = t.replace(/\{\{([^\|}]+)(?:\|([^}]+))*}}/gi, (function(t, s, o) {
                var n = i.helper.namespace.call(i, s, e, "get", "");
                return ~(o = o && o.split("|") || []).indexOf("slugify") && (n = i.helper.slugify.call(i, n)), n
            })) : "function" == typeof t && (t = t.call(this, e)), t
        },
        getMultiselectComparedData: function(t) {
            var e = "";
            if (Array.isArray(this.options.multiselect.matchOn))
                for (var i = 0, s = this.options.multiselect.matchOn.length; i < s; ++i) e += void 0 !== t[this.options.multiselect.matchOn[i]] ? t[this.options.multiselect.matchOn[i]] : "";
            else {
                var o = JSON.parse(JSON.stringify(t)),
                    n = ["group", "matchedKey", "compiled", "href"];
                for (i = 0, s = n.length; i < s; ++i) delete o[n[i]];
                e = JSON.stringify(o)
            }
            return e
        },
        buildBackdropLayout: function() {
            this.options.backdrop && (this.backdrop.container || (this.backdrop.css = t.extend({
                opacity: .6,
                filter: "alpha(opacity=60)",
                position: "fixed",
                top: 0,
                right: 0,
                bottom: 0,
                left: 0,
                "z-index": 1040,
                "background-color": "#000"
            }, this.options.backdrop), this.backdrop.container = t("<div/>", {
                class: this.options.selector.backdrop,
                css: this.backdrop.css
            }).insertAfter(this.container)), this.container.addClass("backdrop").css({
                "z-index": this.backdrop.css["z-index"] + 1,
                position: "relative"
            }))
        },
        buildHintLayout: function(e) {
            if (this.options.hint)
                if (this.node[0].scrollWidth > Math.ceil(this.node.innerWidth())) this.hint.container && this.hint.container.val("");
                else {
                    var i = this,
                        s = "",
                        o = (e = e || this.result, this.query.toLowerCase());
                    if (this.options.accent && (o = this.helper.removeAccent.call(this, o)), this.hintIndex = null, this.searchGroups.length) {
                        if (this.hint.container || (this.hint.css = t.extend({
                                "border-color": "transparent",
                                position: "absolute",
                                top: 0,
                                display: "inline",
                                "z-index": -1,
                                float: "none",
                                color: "silver",
                                "box-shadow": "none",
                                cursor: "default",
                                "-webkit-user-select": "none",
                                "-moz-user-select": "none",
                                "-ms-user-select": "none",
                                "user-select": "none"
                            }, this.options.hint), this.hint.container = t("<" + this.node[0].nodeName + "/>", {
                                type: this.node.attr("type"),
                                class: this.node.attr("class"),
                                readonly: !0,
                                unselectable: "on",
                                "aria-hidden": "true",
                                tabindex: -1,
                                click: function() {
                                    i.node.focus()
                                }
                            }).addClass(this.options.selector.hint).css(this.hint.css).insertAfter(this.node), this.node.parent().css({
                                position: "relative"
                            })), this.hint.container.css("color", this.hint.css.color), o)
                            for (var n, r, a, l = 0, h = e.length; l < h; l++)
                                if (!e[l].disabled) {
                                    r = e[l].group;
                                    for (var c = 0, p = (n = this.options.source[r].display || this.options.display).length; c < p; c++)
                                        if (a = String(e[l][n[c]]).toLowerCase(), this.options.accent && (a = this.helper.removeAccent.call(this, a)), 0 === a.indexOf(o)) {
                                            s = String(e[l][n[c]]), this.hintIndex = l;
                                            break
                                        } if (null !== this.hintIndex) break
                                } var u = s.length > 0 && this.rawQuery + s.substring(this.query.length) || "";
                        this.hint.container.val(u), this.isContentEditable && this.hint.container.text(u)
                    }
                }
        },
        buildDropdownLayout: function() {
            if (this.options.dropdownFilter) {
                var e = this;
                t("<span/>", {
                    class: this.options.selector.filter,
                    html: function() {
                        t(this).append(t("<button/>", {
                            type: "button",
                            class: e.options.selector.filterButton,
                            style: "display: none;",
                            click: function() {
                                e.container.toggleClass("filter");
                                var i = e.namespace + "-dropdown-filter";
                                t("html").off(i), e.container.hasClass("filter") && t("html").on("click" + i + " touchend" + i, (function(s) {
                                    t(s.target).closest("." + e.options.selector.filter)[0] && t(s.target).closest(e.container)[0] || e.hasDragged || (e.container.removeClass("filter"), t("html").off(i))
                                }))
                            }
                        })), t(this).append(t("<ul/>", {
                            class: e.options.selector.dropdown
                        }))
                    }
                }).insertAfter(e.container.find("." + e.options.selector.query))
            }
        },
        buildDropdownItemLayout: function(e) {
            if (this.options.dropdownFilter) {
                var i, s, o = this,
                    n = "string" == typeof this.options.dropdownFilter && this.options.dropdownFilter || "All",
                    r = this.container.find("." + this.options.selector.dropdown);
                "static" !== e || !0 !== this.options.dropdownFilter && "string" != typeof this.options.dropdownFilter || this.dropdownFilter.static.push({
                    key: "group",
                    template: "{{group}}",
                    all: n,
                    value: Object.keys(this.options.source)
                });
                for (var a = 0, l = this.dropdownFilter[e].length; a < l; a++) {
                    s = this.dropdownFilter[e][a], Array.isArray(s.value) || (s.value = [s.value]), s.all && (this.dropdownFilterAll = s.all);
                    for (var h = 0, c = s.value.length; h <= c; h++) h === c && a !== l - 1 || h === c && a === l - 1 && "static" === e && this.dropdownFilter.dynamic.length || (i = this.dropdownFilterAll || n, s.value[h] ? i = s.template ? s.template.replace(new RegExp("{{" + s.key + "}}", "gi"), s.value[h]) : s.value[h] : this.container.find("." + o.options.selector.filterButton).html(i), function(e, i, s) {
                        r.append(t("<li/>", {
                            class: o.options.selector.dropdownItem + " " + o.helper.slugify.call(o, i.key + "-" + (i.value[e] || n)),
                            html: t("<a/>", {
                                href: "javascript:;",
                                html: s,
                                click: function(t) {
                                    t.preventDefault(), p.call(o, {
                                        key: i.key,
                                        value: i.value[e] || "*",
                                        template: s
                                    })
                                }
                            })
                        }))
                    }(h, s, i))
                }
                this.dropdownFilter[e].length && this.container.find("." + o.options.selector.filterButton).removeAttr("style")
            }

            function p(t) {
                "*" === t.value ? delete this.filters.dropdown : this.filters.dropdown = t, this.container.removeClass("filter").find("." + this.options.selector.filterButton).html(t.template), this.isDropdownEvent = !0, this.node.trigger("input" + this.namespace), this.options.multiselect && this.adjustInputSize(), this.node.focus()
            }
        },
        dynamicFilter: {
            isEnabled: !1,
            init: function() {
                this.options.dynamicFilter && (this.dynamicFilter.bind.call(this), this.dynamicFilter.isEnabled = !0)
            },
            validate: function(t) {
                var e, i, s = null,
                    o = null;
                for (var n in this.filters.dynamic)
                    if (this.filters.dynamic.hasOwnProperty(n) && (i = ~n.indexOf(".") ? this.helper.namespace.call(this, n, t, "get") : t[n], "|" !== this.filters.dynamic[n].modifier || s || (s = i == this.filters.dynamic[n].value || !1), "&" === this.filters.dynamic[n].modifier)) {
                        if (i != this.filters.dynamic[n].value) {
                            o = !1;
                            break
                        }
                        o = !0
                    } return e = s, null !== o && (e = o, !0 === o && null !== s && (e = s)), !!e
            },
            set: function(t, e) {
                var i = t.match(/^([|&])?(.+)/);
                e ? this.filters.dynamic[i[2]] = {
                    modifier: i[1] || "|",
                    value: e
                } : delete this.filters.dynamic[i[2]], this.dynamicFilter.isEnabled && this.generateSource()
            },
            bind: function() {
                for (var e, i = this, s = 0, o = this.options.dynamicFilter.length; s < o; s++) "string" == typeof(e = this.options.dynamicFilter[s]).selector && (e.selector = t(e.selector)), e.selector instanceof t && e.selector[0] && e.key ? function(t) {
                    t.selector.off(i.namespace).on("change" + i.namespace, (function() {
                        i.dynamicFilter.set.apply(i, [t.key, i.dynamicFilter.getValue(this)])
                    })).trigger("change" + i.namespace)
                }(e) : this.options.debug && (h.log({
                    node: this.selector,
                    function: "buildDynamicLayout()",
                    message: 'Invalid jQuery selector or jQuery Object for "filter.selector" or missing filter.key'
                }), h.print())
            },
            getValue: function(t) {
                var e;
                return "SELECT" === t.tagName ? e = t.value : "INPUT" === t.tagName && ("checkbox" === t.type ? e = t.checked && t.getAttribute("value") || t.checked || null : "radio" === t.type && t.checked && (e = t.value)), e
            }
        },
        buildMultiselectLayout: function() {
            if (this.options.multiselect) {
                var e, i = this;
                this.label.container = t("<span/>", {
                    class: this.options.selector.labelContainer,
                    "data-padding-left": parseFloat(this.node.css("padding-left")) || 0,
                    "data-padding-right": parseFloat(this.node.css("padding-right")) || 0,
                    "data-padding-top": parseFloat(this.node.css("padding-top")) || 0,
                    click: function(e) {
                        t(e.target).hasClass(i.options.selector.labelContainer) && i.node.focus()
                    }
                }), this.node.closest("." + this.options.selector.query).prepend(this.label.container), this.options.multiselect.data && (Array.isArray(this.options.multiselect.data) ? this.populateMultiselectData(this.options.multiselect.data) : "function" == typeof this.options.multiselect.data && (e = this.options.multiselect.data.call(this), Array.isArray(e) ? this.populateMultiselectData(e) : "function" == typeof e.promise && t.when(e).then((function(t) {
                    t && Array.isArray(t) && i.populateMultiselectData(t)
                }))))
            }
        },
        isMultiselectUniqueData: function(t) {
            for (var e = !0, i = 0, s = this.comparedItems.length; i < s; ++i)
                if (this.comparedItems[i] === this.getMultiselectComparedData(t)) {
                    e = !1;
                    break
                } return e
        },
        populateMultiselectData: function(t) {
            for (var e = 0, i = t.length; e < i; ++e) this.addMultiselectItemLayout(t[e]);
            this.node.trigger("search" + this.namespace, {
                origin: "populateMultiselectData"
            })
        },
        addMultiselectItemLayout: function(e) {
            if (this.isMultiselectUniqueData(e)) {
                this.items.push(e), this.comparedItems.push(this.getMultiselectComparedData(e));
                var i = this.getTemplateValue(e),
                    s = this,
                    o = this.options.multiselect.href ? "a" : "span",
                    n = t("<span/>", {
                        class: this.options.selector.label,
                        html: t("<" + o + "/>", {
                            text: i,
                            click: function(e) {
                                var i = t(this).closest("." + s.options.selector.label),
                                    o = s.label.container.find("." + s.options.selector.label).index(i);
                                s.options.multiselect.callback && s.helper.executeCallback.call(s, s.options.multiselect.callback.onClick, [s.node, s.items[o], e])
                            },
                            href: this.options.multiselect.href ? function(t) {
                                return s.generateHref.call(s, s.options.multiselect.href, t)
                            }(s.items[s.items.length - 1]) : null
                        })
                    });
                return n.append(t("<span/>", {
                    class: this.options.selector.cancelButton,
                    html: "Ã—",
                    click: function(e) {
                        var i = t(this).closest("." + s.options.selector.label),
                            o = s.label.container.find("." + s.options.selector.label).index(i);
                        s.cancelMultiselectItem(o, i, e)
                    }
                })), this.label.container.append(n), this.adjustInputSize(), !0
            }
        },
        cancelMultiselectItem: function(t, e, i) {
            var s = this.items[t];
            (e = e || this.label.container.find("." + this.options.selector.label).eq(t)).remove(), this.items.splice(t, 1), this.comparedItems.splice(t, 1), this.options.multiselect.callback && this.helper.executeCallback.call(this, this.options.multiselect.callback.onCancel, [this.node, s, i]), this.adjustInputSize(), this.focusOnly = !0, this.node.focus().trigger("input" + this.namespace, {
                origin: "cancelMultiselectItem"
            })
        },
        adjustInputSize: function() {
            var e = this.node[0].getBoundingClientRect().width - (parseFloat(this.label.container.data("padding-right")) || 0) - (parseFloat(this.label.container.css("padding-left")) || 0),
                i = 0,
                s = 0,
                o = 0,
                n = !1,
                r = 0;
            this.label.container.find("." + this.options.selector.label).filter((function(a, l) {
                0 === a && (r = t(l)[0].getBoundingClientRect().height + parseFloat(t(l).css("margin-bottom") || 0)), i = t(l)[0].getBoundingClientRect().width + parseFloat(t(l).css("margin-right") || 0), o + i > .7 * e && !n && (s++, n = !0), o + i < e ? o += i : (n = !1, o = i)
            }));
            var a = parseFloat(this.label.container.data("padding-left") || 0) + (n ? 0 : o),
                l = s * r + parseFloat(this.label.container.data("padding-top") || 0);
            this.container.find("." + this.options.selector.query).find("input, textarea, [contenteditable], .typeahead__hint").css({
                paddingLeft: a,
                paddingTop: l
            })
        },
        showLayout: function() {
            !this.container.hasClass("result") && (this.result.length || this.displayEmptyTemplate || this.options.backdropOnFocus) && (function() {
                var e = this;
                t("html").off("keydown" + this.namespace).on("keydown" + this.namespace, (function(i) {
                    i.keyCode && 9 === i.keyCode && setTimeout((function() {
                        t(":focus").closest(e.container).find(e.node)[0] || e.hideLayout()
                    }), 0)
                })), t("html").off("click" + this.namespace + " touchend" + this.namespace).on("click" + this.namespace + " touchend" + this.namespace, (function(i) {
                    t(i.target).closest(e.container)[0] || t(i.target).closest("." + e.options.selector.item)[0] || i.target.className === e.options.selector.cancelButton || e.hasDragged || e.hideLayout()
                }))
            }.call(this), this.container.addClass([this.result.length || this.searchGroups.length && this.displayEmptyTemplate ? "result " : "", this.options.hint && this.searchGroups.length ? "hint" : "", this.options.backdrop || this.options.backdropOnFocus ? "backdrop" : ""].join(" ")), this.helper.executeCallback.call(this, this.options.callback.onShowLayout, [this.node, this.query]))
        },
        hideLayout: function() {
            (this.container.hasClass("result") || this.container.hasClass("backdrop")) && (this.container.removeClass("result hint filter" + (this.options.backdropOnFocus && t(this.node).is(":focus") ? "" : " backdrop")), this.options.backdropOnFocus && this.container.hasClass("backdrop") || (t("html").off(this.namespace), this.helper.executeCallback.call(this, this.options.callback.onHideLayout, [this.node, this.query])))
        },
        resetLayout: function() {
            this.result = [], this.tmpResult = {}, this.groups = [], this.resultCount = 0, this.resultCountPerGroup = {}, this.resultItemCount = 0, this.resultHtml = null, this.options.hint && this.hint.container && (this.hint.container.val(""), this.isContentEditable && this.hint.container.text(""))
        },
        resetInput: function() {
            this.node.val(""), this.isContentEditable && this.node.text(""), this.query = "", this.rawQuery = ""
        },
        buildCancelButtonLayout: function() {
            if (this.options.cancelButton) {
                var e = this;
                t("<span/>", {
                    class: this.options.selector.cancelButton,
                    html: "Ã—",
                    mousedown: function(t) {
                        t.stopImmediatePropagation(), t.preventDefault(), e.resetInput(), e.node.trigger("input" + e.namespace, [t])
                    }
                }).insertBefore(this.node)
            }
        },
        toggleCancelButtonVisibility: function() {
            this.container.toggleClass("cancel", !!this.query.length)
        },
        __construct: function() {
            this.extendOptions(), this.unifySourceFormat() && (this.dynamicFilter.init.apply(this), this.init(), this.buildDropdownLayout(), this.buildDropdownItemLayout("static"), this.buildMultiselectLayout(), this.delegateEvents(), this.buildCancelButtonLayout(), this.helper.executeCallback.call(this, this.options.callback.onReady, [this.node]))
        },
        helper: {
            isEmpty: function(t) {
                for (var e in t)
                    if (t.hasOwnProperty(e)) return !1;
                return !0
            },
            removeAccent: function(t) {
                if ("string" == typeof t) {
                    var e = s;
                    return "object" == typeof this.options.accent && (e = this.options.accent), t = t.toLowerCase().replace(new RegExp("[" + e.from + "]", "g"), (function(t) {
                        return e.to[e.from.indexOf(t)]
                    }))
                }
            },
            slugify: function(t) {
                return "" !== (t = String(t)) && (t = (t = this.helper.removeAccent.call(this, t)).replace(/[^-a-z0-9]+/g, "-").replace(/-+/g, "-").replace(/^-|-$/g, "")), t
            },
            sort: function(t, e, i) {
                var s = function(e) {
                    for (var s = 0, o = t.length; s < o; s++)
                        if (void 0 !== e[t[s]]) return i(e[t[s]]);
                    return e
                };
                return e = [-1, 1][+!!e],
                    function(t, i) {
                        return t = s(t), i = s(i), e * ((t > i) - (i > t))
                    }
            },
            replaceAt: function(t, e, i, s) {
                return t.substring(0, e) + s + t.substring(e + i)
            },
            highlight: function(t, e, i) {
                t = String(t);
                var s = i && this.helper.removeAccent.call(this, t) || t,
                    o = [];
                Array.isArray(e) || (e = [e]), e.sort((function(t, e) {
                    return e.length - t.length
                }));
                for (var n = e.length - 1; n >= 0; n--) "" !== e[n].trim() ? e[n] = e[n].replace(/[-[\]{}()*+?.,\\^$|#\s]/g, "\\$&") : e.splice(n, 1);
                for (s.replace(new RegExp("(?:" + e.join("|") + ")(?!([^<]+)?>)", "gi"), (function(t, e, i) {
                        o.push({
                            offset: i,
                            length: t.length
                        })
                    })), n = o.length - 1; n >= 0; n--) t = this.helper.replaceAt(t, o[n].offset, o[n].length, "<strong>" + t.substr(o[n].offset, o[n].length) + "</strong>");
                return t
            },
            getCaret: function(t) {
                var e = 0;
                if (t.selectionStart) return t.selectionStart;
                if (document.selection) {
                    var i = document.selection.createRange();
                    if (null === i) return e;
                    var s = t.createTextRange(),
                        o = s.duplicate();
                    s.moveToBookmark(i.getBookmark()), o.setEndPoint("EndToStart", s), e = o.text.length
                } else if (window.getSelection) {
                    var n = window.getSelection();
                    if (n.rangeCount) {
                        var r = n.getRangeAt(0);
                        r.commonAncestorContainer.parentNode == t && (e = r.endOffset)
                    }
                }
                return e
            },
            setCaretAtEnd: function(t) {
                if (void 0 !== window.getSelection && void 0 !== document.createRange) {
                    var e = document.createRange();
                    e.selectNodeContents(t), e.collapse(!1);
                    var i = window.getSelection();
                    i.removeAllRanges(), i.addRange(e)
                } else if (void 0 !== document.body.createTextRange) {
                    var s = document.body.createTextRange();
                    s.moveToElementText(t), s.collapse(!1), s.select()
                }
            },
            cleanStringFromScript: function(t) {
                return "string" == typeof t && t.replace(/<\/?(?:script|iframe)\b[^>]*>/gm, "") || t
            },
            executeCallback: function(t, e) {
                if (t) {
                    var i;
                    if ("function" == typeof t) i = t;
                    else if (("string" == typeof t || Array.isArray(t)) && ("string" == typeof t && (t = [t, []]), "function" != typeof(i = this.helper.namespace.call(this, t[0], window)))) return void(this.options.debug && (h.log({
                        node: this.selector,
                        function: "executeCallback()",
                        arguments: JSON.stringify(t),
                        message: 'WARNING - Invalid callback function"'
                    }), h.print()));
                    return i.apply(this, (t[1] || []).concat(e || []))
                }
            },
            namespace: function(t, e, i, s) {
                if ("string" != typeof t || "" === t) return this.options.debug && (h.log({
                    node: this.options.input || this.selector,
                    function: "helper.namespace()",
                    arguments: t,
                    message: 'ERROR - Missing string"'
                }), h.print()), !1;
                var o = void 0 !== s ? s : void 0;
                if (!~t.indexOf(".")) return e[t] || o;
                for (var n = t.split("."), r = e || window, a = (i = i || "get", ""), l = 0, c = n.length; l < c; l++) {
                    if (void 0 === r[a = n[l]]) {
                        if (~["get", "delete"].indexOf(i)) return void 0 !== s ? s : void 0;
                        r[a] = {}
                    }
                    if (~["set", "create", "delete"].indexOf(i) && l === c - 1) {
                        if ("set" !== i && "create" !== i) return delete r[a], !0;
                        r[a] = o
                    }
                    r = r[a]
                }
                return r
            },
            typeWatch: (e = 0, function(t, i) {
                clearTimeout(e), e = setTimeout(t, i)
            })
        }
    }, t.fn.typeahead = t.typeahead = function(t) {
        return l.typeahead(this, t)
    };
    var l = {
            typeahead: function(e, i) {
                if (!i || !i.source || "object" != typeof i.source) return h.log({
                    node: e.selector || i && i.input,
                    function: "$.typeahead()",
                    arguments: JSON.stringify(i && i.source || ""),
                    message: 'Undefined "options" or "options.source" or invalid source type - Typeahead dropped'
                }), void h.print();
                if ("function" == typeof e) {
                    if (!i.input) return h.log({
                        node: e.selector,
                        function: "$.typeahead()",
                        message: 'Undefined "options.input" - Typeahead dropped'
                    }), void h.print();
                    e = t(i.input)
                }
                if (!e.length) return h.log({
                    node: e.selector,
                    function: "$.typeahead()",
                    arguments: JSON.stringify(i.input),
                    message: "Unable to find jQuery input element - Typeahead dropped"
                }), void h.print();
                if (void 0 === e[0].value && (e[0].value = e.text()), 1 === e.length) return e[0].selector = e.selector || i.input || e[0].nodeName.toLowerCase(), window.Typeahead[e[0].selector] = new a(e, i);
                for (var s, o = {}, n = 0, r = e.length; n < r; ++n) void 0 !== o[s = e[n].nodeName.toLowerCase()] && (s += n), e[n].selector = s, window.Typeahead[s] = o[s] = new a(e.eq(n), i);
                return o
            }
        },
        h = {
            table: {},
            log: function(e) {
                e.message && "string" == typeof e.message && (this.table[e.message] = t.extend({
                    node: "",
                    function: "",
                    arguments: ""
                }, e))
            },
            print: function() {
                !a.prototype.helper.isEmpty(this.table) && console && console.table && (this.table = {})
            }
        };
    return h.print(), window.console = window.console || {
        log: function() {}
    }, Array.isArray || (Array.isArray = function(t) {
        return "[object Array]" === Object.prototype.toString.call(t)
    }), "trim" in String.prototype || (String.prototype.trim = function() {
        return this.replace(/^\s+/, "").replace(/\s+$/, "")
    }), "indexOf" in Array.prototype || (Array.prototype.indexOf = function(t, e) {
        void 0 === e && (e = 0), e < 0 && (e += this.length), e < 0 && (e = 0);
        for (var i = this.length; e < i; e++)
            if (e in this && this[e] === t) return e;
        return -1
    }), Object.keys || (Object.keys = function(t) {
        var e, i = [];
        for (e in t) Object.prototype.hasOwnProperty.call(t, e) && i.push(e);
        return i
    }), a
}, "function" == typeof define && define.amd ? define("jquery-typeahead", ["jquery"], (function(e) {
    return t(e)
})) : "object" == typeof module && module.exports ? module.exports = function(e, i) {
    return void 0 === e && (e = "undefined" != typeof window ? require("jquery") : require("jquery")(void 0)), t(e)
}() : t(jQuery);