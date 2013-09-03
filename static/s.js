(function() {
	(function(e) {
		e.tweetFeed = function(t, n) {
			var i, r, s;
			s = this;
			s.$el = e(t);
			s.el = t;
			s.$el.data("tweetFeed", s);
			r = {
				getUserTweets : function(t) {
					var n, i, r, s, a = this;
					i = t.body;
					i = this._removeImages(i);
					n = e(i);
					r = [];
					s = n.find("li.tweet");
					this._each(s, function(e) {
						return r.push(a._getDataFromTweetEl(e))
					});
					t = {};
					t.results = r;
					return t
				},
				_getDataFromTweetEl : function(t) {
					var n, i;
					n = e(t);
					i = {};
					i.created_at = n.find("a.permalink").attr("data-datetime");
					i.from_user = n.find(".p-nickname b").text();
					i.profile_image_url = n.find(".avatar").attr("data-src");
					i.id_str = n.attr("data-tweet-id");
					i.text = n.find(".e-entry-title").text();
					return i
				},
				_removeImages : function(e) {
					e = e.replace(/<img/gm, "<div");
					e = e.replace(/<\/img/gm, "</div");
					e = e.replace(/src="/gm, 'data-src="');
					return e
				},
				_each : function(e, t) {
					var n, i;
					n = 0;
					i = [];
					while (n < e.length) {
						t(e[n]);
						i.push(n++)
					}
					return i
				}
			};
			i = {
				months : {
					0 : "january",
					1 : "february",
					2 : "march",
					3 : "april",
					4 : "may",
					5 : "june",
					6 : "july",
					7 : "august",
					8 : "september",
					9 : "october",
					10 : "november",
					11 : "december"
				},
				days : {
					0 : "sun",
					1 : "mon",
					2 : "tues",
					3 : "wed",
					4 : "thu",
					5 : "fri",
					6 : "sat"
				},
				defaultOptions : {
					feedType : "search",
					userName : "jquery",
					searchTerms : ["javascript", "jquery", "html5", "css3", "java"],
					searchTermsWithAnd : [],
					pollInterval : 10,
					resultType : "recent",
					maxTweets : 3,
					stopPollOnHover : true,
					height :
					void 0,
					width : false
				},
				currentRecentId : 0,
				showFeed : function(e) {
					var t, n = this;
					this.options = e || {};
					this._setDefaultOptions(this.options);
					s.$el.append(this._getContainerTemplate());
					t = function() {
						return n._requestFeed()
					};
					t();
					this._bindInitialEvents();
					this._bindEvents();
					return this._sizeOuter()
				},
				startPolling : function() {
					var e, t = this;
					e = function() {
						return t._requestFeed()
					};
					if (this.options.pollInterval) {
						return this.interval = setInterval(e, this.options.pollInterval * 1e3)
					}
				},
				_sizeOuter : function() {
					s.$el.find(".tweetfeed-list-container-wrapper").css({
						height : this.options.height || 150 * this.options.maxTweets,
						"overflow-y" : "hidden"
					});
					if (this.options.width) {
						return s.$el.find(".tweetfeed-list-container-wrapper").css({
							width : this.options.width
						})
					}
				},
				_getItemTemplate : function(e) {
					var t, n, i, r;
					t = new Date(this._parseDate(e.created_at));
					n = this.days[t.getDay()];
					r = this.months[t.getMonth()];
					i = t.getDate();
					return '<div class="tweetfeed-item-container tweetfeed-non-fixed tweetfeed-new-item">\n  <div class="tweetfeed-time-bar"></div>\n  <a href="http://www.twitter.com/' + e.from_user + '" rel="nofollow" target="_blank">\n    <div class="tweetfeed-author-container">\n      <div class="tweetfeed-author-img-container" style="background-image: url(' + e.profile_image_url + ');">\n      </div>\n    </div>\n  </a>\n  <a href="http://www.twitter.com/' + e.from_user + "/status/" + e.id_str + '" target="_blank">\n  <div class="tweetfeed-item-content-container tweetfeed-unbound" data-item-id="' + e.id_str + '" data-username="' + e.from_user + '">\n      <div class="tweetfeed-triangle-background"></div>\n      <div class="tweetfeed-triangle"></div>\n      <div class="tweetfeed-author-name-container">\n        <span class="tweetfeed-author-name"><span class="tweetfeed-at-sign">@</span>' + e.from_user + '</span>\n      </div>\n      <div class="tweetfeed-date-container">\n        <span class="tweetfeed-day-of-month">' + i + '</span>\n        <span class="tweetfeed-month">' + r + '</span>\n        <span class="tweetfeed-day">' + n + '</span>\n      </div>\n      <div class="tweetfeed-item-content">\n        <div class="tweetfeed-tweet-content">' + e.text + "</div>\n      </div>\n  </div>\n  </a>\n</div>\n"
				},
				_getContainerTemplate : function() {
					return '<div class="tweetfeed-list-container-wrapper">\n  <div class="tweetfeed-list-container">\n  </div>\n</div>'
				},
				_requestFeed : function() {
					var t, n, i = this;
					n = this._getUrl();
					t = {
						url : n,
						dataType : "jsonp",
						success : function(e) {
							var t, n, a;
							if ((e != null ? ( n = e.headers) != null ? ( a = n.message) != null ? a.length :
							void 0 :
							void 0 :
							void 0) > 0) {
								throw new Error(e.headers.message)
							} else {
								e = r.getUserTweets(e);
								t = parseInt(e.results[0].id_str);
								if (t > i.currentRecentId) {
									i.currentRecentId = t;
									s.$el.find(".tweetfeed-list-container").prepend(i._getListTemplate(e.results));
									return i._afterGotFeed()
								}
							}
						}
					};
					return e.ajax(t)
				},
				_bindInitialEvents : function() {
					var e, t, n = this;
					if (this.options.stopPollOnHover) {
						e = function() {
							return n._onMouseEnter()
						};
						s.$el.mouseenter(e);
						t = function() {
							return n._onMouseOut()
						};
						return s.$el.mouseleave(t)
					}
				},
				_bindEvents : function() {
					var e = this;
					s.$el.find(".tweetfeed-item-content-container.tweetfeed-unbound").click(function(t) {
						return e._onClickTweet(t)
					});
					return s.$el.find(".tweetfeed-item-content-container.tweetfeed-unbound").removeClass("unbound")
				},
				_afterGotFeed : function() {
					if (this.interval ===
					void 0) {
						this.startPolling()
					}
					this._removeBottomTweets();
					this._bindEvents();
					return this._animateNewItems()
				},
				_onClickTweet : function(t) {
					var n, i, r, s;
					n = e(t.currentTarget);
					r = t.srcElement;
					if (r.nodeName.toLowerCase().match(/$a^/) === null) {
						s = n.attr("data-username");
						return i = n.attr("data-item-id")
					}
				},
				_onScrollContainer : function() {
					var e;
					e = s.$el.find(".tweetfeed-item-container.tweetfeed-non-fixed:first").position().top;
					if (e <= 4) {
						s.$el.find(".tweetfeed-item-container.tweetfeed-non-fixed:first").addClass("tweetfeed-fixed");
						return s.$el.find(".tweetfeed-item-container.tweetfeed-non-fixed:first").removeClass("tweetfeed-non-fixed")
					}
				},
				_onMouseEnter : function(e) {
					return clearInterval(this.interval)
				},
				_onMouseOut : function(e) {
					return this.startPolling()
				},
				_removeBottomTweets : function() {
					if (this.options.maxTweets) {
						if (s.$el.find(".tweetfeed-item-container").length > this.options.maxTweets) {
							return s.$el.find(".tweetfeed-item-container:gt(" + (this.options.maxTweets - 1) + ")").remove()
						}
					}
				},
				_getUrl : function() {
					if (this.options.widgetId) {
						return "http://cdn.syndication.twimg.com/widgets/timelines/" + this.options.widgetId + "?domain=" + window.location.host + "&lang=en&suppress_response_codes=true"
					} else {
						throw new Error("In order to use the tweet feed plugin, you must provide the twitter widget id for your widget.  See the documentation for more information about obtaining a widget id.")
					}
				},
				_getListTemplate : function(e) {
					var t, n, i;
					i = "";
					t = 0;
					while (t < e.length) {
						n = e[t];
						i += this._getItemTemplate(n);
						t++
					}
					return i
				},
				_setDefaultOptions : function(e) {
					var t, n;
					n = [];
					for (t in this.defaultOptions) {
						if (e[t] ===
						void 0) {
							n.push(e[t] = this.defaultOptions[t])
						} else {
							n.push(
							void 0)
						}
					}
					return n
				},
				_parseDate : function(e) {
					var t;
					e = e.replace(/T.*/, "");
					t = e.match(/[0-9][0-9][0-9][0-9]-/);
					if (t) {
						e = e.replace(t[0], "");
						e += "-" + t[0];
						e = e.substr(0, e.length - 1);
						e = e.replace(/-/g, "/")
					}
					return Date.parse(e)
				},
				_animateNewItems : function() {
					var t, n, i;
					t = e.browser.msie && parseInt(e.browser.version, 10) < 10;
					n = e.browser.mozilla && parseInt(e.browser.version, 10) < 4;
					i = e.browser.opera && parseInt(e.browser.version, 10) < 11;
					if (t || n || i) {
						return this._doJqueryAnimate()
					} else {
						return this._doCSS3Animate()
					}
				},
				_doCSS3Animate : function() {
					var e, t, n, i = this;
					t = s.$el.find(".tweetfeed-new-item").height();
					e = function() {
						var e;
						s.$el.find(".tweetfeed-new-item").removeAttr("style");
						s.$el.find(".tweetfeed-new-item").find(".tweetfeed-item-content-container").removeClass("tweetfeed-flag-animate");
						e = function() {
							return s.$el.find(".tweetfeed-new-item").find(".tweetfeed-item-content-container").css({
								"-webkit-transform" : "scaleX(1)",
								"-o-transform" : "scaleX(1)",
								"-moz-transform" : "scaleX(1)",
								transform : "scaleX(1)"
							})
						};
						setTimeout(e, 1);
						return s.$el.find(".tweetfeed-new-item").removeClass("tweetfeed-new-item")
					};
					s.$el.find(".tweetfeed-new-item").find(".tweetfeed-item-content-container").addClass("tweetfeed-flag-animate");
					s.$el.find(".tweetfeed-new-item").css({
						height : 0
					});
					n = function() {
						return s.$el.find(".tweetfeed-new-item").css({
							"-webkit-transition" : "all .5s",
							"-o-transition" : "all .5s",
							"-moz-transition" : "all .5s",
							transition : "all .5s",
							height : t
						})
					};
					setTimeout(n, 1);
					return setTimeout(e, 500)
				},
				_doJqueryAnimate : function() {
					var e, t, n = this;
					e = function() {
						s.$el.find(".tweetfeed-new-item").removeAttr("style");
						return s.$el.find(".tweetfeed-new-item").removeClass("tweetfeed-new-item")
					};
					s.$el.find(".tweetfeed-new-item").find(".tweetfeed-item-content-container").css({
						opacity : 0
					});
					t = s.$el.find(".tweetfeed-new-item").height();
					s.$el.find(".tweetfeed-new-item").css({
						height : 0,
						"overflow-y" : "hidden"
					}).animate({
						height : t
					}, 500, e);
					return s.$el.find(".tweetfeed-new-item").find(".tweetfeed-item-content-container").animate({
						opacity : 1
					}, 500)
				}
			};
			return i.showFeed(n)
		};
		return e.fn.tweetFeed = function(t) {
			return this.each(function() {
				return new e.tweetFeed(this, t)
			})
		}
	})(window.jQuery)
}).call(this);

