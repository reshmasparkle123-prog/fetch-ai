"""Chat replies in English / Telugu / Hindi, rendered from the internal agents' structured results."""

import ration_data as rd

T = {
    "welcome": {
        "en": ("Namaste! I'm **RationSeva**, your fair-price (ration) shop helper. I can:\n"
               "• Check stock — \"Is rice available at shop 0306122?\"\n"
               "• Find other shops — \"Rice is low at my shop 0306122, where else can I go?\"\n"
               "• Make a stock notice poster — \"Make a Telugu stock notice for 0306122\"\n"
               "• Check your ration weight — attach a photo of the scale with your shop number and entitled kg.\n"
               "I understand English, తెలుగు and हिंदी."),
        "te": ("నమస్తే! నేను **రేషన్ సేవ**, మీ రేషన్ షాప్ సహాయకుడిని. నేను:\n"
               "• నిల్వ చూపిస్తాను — \"0306122 షాప్‌లో బియ్యం ఉందా?\"\n"
               "• వేరే షాపులు చెబుతాను — \"నా షాప్ 0306122 లో బియ్యం తక్కువగా ఉంది, ఇంకెక్కడ దొరుకుతుంది?\"\n"
               "• స్టాక్ నోటీసు తయారు చేస్తాను — \"0306122 కి తెలుగు నోటీసు చేయండి\"\n"
               "• తూకం చెక్ చేస్తాను — స్కేల్ ఫోటో, షాప్ నంబర్, మీకు రావాల్సిన కిలోలు పంపండి."),
        "hi": ("नमस्ते! मैं **राशन सेवा** हूँ, आपकी राशन दुकान का सहायक। मैं:\n"
               "• स्टॉक बताता हूँ — \"दुकान 0306122 में चावल है क्या?\"\n"
               "• दूसरी दुकानें बताता हूँ — \"मेरी दुकान 0306122 में चावल कम है, और कहाँ मिलेगा?\"\n"
               "• स्टॉक नोटिस बनाता हूँ — \"0306122 के लिए हिंदी नोटिस बनाओ\"\n"
               "• तौल जाँचता हूँ — तराज़ू की फोटो, दुकान नंबर और आपको मिलने वाले किलो भेजें।"),
    },
    "ask_fps": {
        "en": "Which shop? Please send your 7-digit fair-price shop (FPS) number, e.g. 0306122.",
        "te": "ఏ షాప్? దయచేసి మీ 7 అంకెల రేషన్ షాప్ (FPS) నంబర్ పంపండి, ఉదా: 0306122.",
        "hi": "कौन-सी दुकान? कृपया अपनी 7 अंकों की राशन दुकान (FPS) संख्या भेजें, जैसे 0306122.",
    },
    "not_found": {
        "en": ("I couldn't find shop **{fps}** in our data. We cover the {n} fair-price shops of Alluri Sitharama "
               "Raju district (AP AePDS report, {time}). Please check the number on your ration card or the shop board."),
        "te": ("షాప్ **{fps}** మా డేటాలో లేదు. మా వద్ద అల్లూరి సీతారామరాజు జిల్లాలోని {n} రేషన్ షాపుల సమాచారం ఉంది "
               "(AP AePDS నివేదిక, {time}). దయచేసి మీ రేషన్ కార్డు లేదా షాప్ బోర్డుపై నంబర్ సరిచూసుకోండి."),
        "hi": ("दुकान **{fps}** हमारे डेटा में नहीं मिली। हमारे पास अल्लूरी सीताराम राजू ज़िले की {n} राशन दुकानों का "
               "डेटा है (AP AePDS रिपोर्ट, {time})। कृपया राशन कार्ड या दुकान के बोर्ड पर नंबर जाँचें।"),
    },
    "shop_header": {
        "en": "**Shop {fps}** — {afso} AFSO, {district}",
        "te": "**షాప్ {fps}** — {afso} AFSO, {district}",
        "hi": "**दुकान {fps}** — {afso} AFSO, {district}",
    },
    "no_item": {
        "en": "This shop has no {item} in this month's report (not allotted).",
        "te": "ఈ నెల నివేదికలో ఈ షాప్‌కి {item} కేటాయించలేదు.",
        "hi": "इस महीने की रिपोर्ट में इस दुकान को {item} आवंटित नहीं है।",
    },
    "AVAILABLE": {"en": "available", "te": "అందుబాటులో ఉంది", "hi": "उपलब्ध"},
    "LOW": {"en": "**LOW**", "te": "**తక్కువగా ఉంది**", "hi": "**कम बचा है**"},
    "OUT_OF_STOCK": {"en": "**OUT OF STOCK**", "te": "**నిల్వ లేదు**", "hi": "**स्टॉक खत्म**"},
    "pct": {
        "en": "only {p}% of this month's stock left",
        "te": "ఈ నెల నిల్వలో {p}% మాత్రమే మిగిలింది",
        "hi": "इस महीने के स्टॉक का केवल {p}% बचा",
    },
    "KG": {"en": "kg", "te": "కిలోలు", "hi": "किलो"},
    "PKT": {"en": "pkts", "te": "ప్యాకెట్లు", "hi": "पैकेट"},
    "alt_header": {
        "en": "Other shops in {afso} AFSO with {item} available:",
        "te": "{afso} AFSO లో {item} అందుబాటులో ఉన్న ఇతర షాపులు:",
        "hi": "{afso} AFSO में {item} वाली अन्य दुकानें:",
    },
    "alt_none": {
        "en": "No other shop in {afso} AFSO has {item} available in this report.",
        "te": "ఈ నివేదిక ప్రకారం {afso} AFSO లో {item} ఉన్న వేరే షాప్ లేదు.",
        "hi": "इस रिपोर्ट के अनुसार {afso} AFSO में किसी और दुकान में {item} उपलब्ध नहीं है।",
    },
    "alt_all_ok": {
        "en": "Good news: every ration item at shop {fps} is available in this report — no need to go elsewhere.",
        "te": "శుభవార్త: ఈ నివేదిక ప్రకారం షాప్ {fps} లో అన్ని సరుకులు అందుబాటులో ఉన్నాయి.",
        "hi": "अच्छी खबर: इस रिपोर्ट के अनुसार दुकान {fps} में सारा राशन उपलब्ध है।",
    },
    "alt_own_ok": {
        "en": "Note: {item} is still available at your shop {fps} in this report.",
        "te": "గమనిక: ఈ నివేదిక ప్రకారం మీ షాప్ {fps} లో {item} ఇంకా అందుబాటులో ఉంది.",
        "hi": "ध्यान दें: इस रिपोर्ट के अनुसार आपकी दुकान {fps} में {item} अभी उपलब्ध है।",
    },
    "portability": {
        "en": "With ration-card portability you can collect at another fair-price shop — carry your ration card.",
        "te": "రేషన్ కార్డు పోర్టబిలిటీతో వేరే రేషన్ షాప్‌లో కూడా సరుకులు తీసుకోవచ్చు — మీ కార్డు తీసుకెళ్లండి.",
        "hi": "राशन कार्ड पोर्टेबिलिटी से आप दूसरी राशन दुकान से भी राशन ले सकते हैं — अपना राशन कार्ड साथ रखें।",
    },
    "footer": {
        "en": "_Data: {source}, {time} — a dated snapshot, not live. Please confirm at the shop._",
        "te": "_సమాచారం: {source}, {time} — ఇది పాత స్నాప్‌షాట్, లైవ్ కాదు. దయచేసి షాప్ వద్ద నిర్ధారించుకోండి._",
        "hi": "_जानकारी: {source}, {time} — यह पुराना स्नैपशॉट है, लाइव नहीं। कृपया दुकान पर पुष्टि करें।_",
    },
    "analysis_down": {
        "en": "_(Shortage analysis is unavailable right now — showing the report status only.)_",
        "te": "_(కొరత విశ్లేషణ ప్రస్తుతం అందుబాటులో లేదు — నివేదికలోని స్థితి మాత్రమే చూపిస్తున్నాం.)_",
        "hi": "_(कमी विश्लेषण अभी उपलब्ध नहीं है — केवल रिपोर्ट की स्थिति दिखा रहे हैं।)_",
    },
    "service_down": {
        "en": "Sorry — the {service} is not responding right now. Please try again in a minute.",
        "te": "క్షమించండి — {service} ప్రస్తుతం స్పందించడం లేదు. ఒక నిమిషం తర్వాత మళ్లీ ప్రయత్నించండి.",
        "hi": "क्षमा करें — {service} अभी जवाब नहीं दे रही है। कृपया एक मिनट बाद फिर कोशिश करें।",
    },
    "svc_stock": {"en": "stock service", "te": "స్టాక్ సేవ", "hi": "स्टॉक सेवा"},
    "svc_notice": {"en": "notice service", "te": "నోటీసు సేవ", "hi": "नोटिस सेवा"},
    "svc_weighing": {"en": "weighing-check service", "te": "తూకం తనిఖీ సేవ", "hi": "तौल जाँच सेवा"},
    "notice_ready": {
        "en": "Stock notice for shop {fps} ({lang_name}) — ready to share on WhatsApp:",
        "te": "షాప్ {fps} స్టాక్ నోటీసు ({lang_name}) సిద్ధం — WhatsApp లో షేర్ చేయండి:",
        "hi": "दुकान {fps} का स्टॉक नोटिस ({lang_name}) तैयार है — WhatsApp पर शेयर करें:",
    },
    "notice_link": {"en": "Open / download the image", "te": "చిత్రం తెరవండి / డౌన్‌లోడ్ చేయండి", "hi": "चित्र खोलें / डाउनलोड करें"},
    "notice_more": {
        "en": "_Rendered by Cloudinary from the AP AePDS report of {time}. Also available in Telugu, Hindi and English — just ask._",
        "te": "_{time} నాటి AP AePDS నివేదిక నుండి Cloudinary ద్వారా తయారైంది. హిందీ, ఇంగ్లీష్‌లో కూడా అడగవచ్చు._",
        "hi": "_{time} की AP AePDS रिपोर्ट से Cloudinary द्वारा बनाया गया। तेलुगु और अंग्रेज़ी में भी माँग सकते हैं।_",
    },
    "notice_empty": {
        "en": "Shop {fps} has no available ration items in this report, so there is nothing to put on a notice.",
        "te": "ఈ నివేదిక ప్రకారం షాప్ {fps} లో అందుబాటులో ఉన్న సరుకులు లేవు, కాబట్టి నోటీసు తయారు చేయలేము.",
        "hi": "इस रिपोर्ट के अनुसार दुकान {fps} में कोई राशन उपलब्ध नहीं है, इसलिए नोटिस नहीं बन सकता।",
    },
    "fallback_text": {
        "en": "Here is the stock as text instead:",
        "te": "బదులుగా నిల్వ వివరాలు ఇక్కడ:",
        "hi": "इसके बदले स्टॉक की जानकारी यहाँ है:",
    },
    "lang_names": {
        "en": {"te": "Telugu", "hi": "Hindi", "en": "English"},
        "te": {"te": "తెలుగు", "hi": "హిందీ", "en": "ఇంగ్లీష్"},
        "hi": {"te": "तेलुगु", "hi": "हिंदी", "en": "अंग्रेज़ी"},
    },
    # ---- weighing ----
    "ask_photo_or_weight": {
        "en": ("To check your ration weight, attach a photo of the weighing-scale display here, or type the weight "
               "you received. Also tell me your shop number and how many kg you are entitled to, "
               "e.g. \"shop 0306122, entitled 20 kg rice\"."),
        "te": ("తూకం తనిఖీ కోసం, స్కేల్ డిస్‌ప్లే ఫోటో ఇక్కడ జత చేయండి, లేదా మీకు వచ్చిన బరువు టైప్ చేయండి. "
               "మీ షాప్ నంబర్, మీకు రావాల్సిన కిలోలు కూడా చెప్పండి, ఉదా: \"షాప్ 0306122, 20 కిలోలు రావాలి\"."),
        "hi": ("तौल जाँच के लिए तराज़ू के डिस्प्ले की फोटो यहाँ भेजें, या आपको मिला वज़न लिखें। अपनी दुकान का नंबर "
               "और आपको कितने किलो मिलने चाहिए, यह भी बताएँ, जैसे \"दुकान 0306122, 20 किलो मिलना चाहिए\"।"),
    },
    "photo_received": {"en": "📷 Photo received. ", "te": "📷 ఫోటో అందింది. ", "hi": "📷 फोटो मिल गई। "},
    "please_tell": {"en": "Please tell me {x}.", "te": "దయచేసి {x} చెప్పండి.", "hi": "कृपया {x} बताएँ।"},
    "and": {"en": " and ", "te": " మరియు ", "hi": " और "},
    "need_fps": {"en": "your 7-digit shop number", "te": "మీ 7 అంకెల షాప్ నంబర్", "hi": "अपनी 7 अंकों की दुकान संख्या"},
    "need_expected": {
        "en": "how many kg you are entitled to (e.g. 20 kg)",
        "te": "మీకు ఎన్ని కిలోలు రావాలి (ఉదా: 20 కిలోలు)",
        "hi": "आपको कितने किलो मिलने चाहिए (जैसे 20 किलो)",
    },
    "OK": {
        "en": "✅ **Weight OK** — weighed {r} kg, entitled {e} kg.",
        "te": "✅ **తూకం సరిగ్గా ఉంది** — తూకం {r} కిలోలు, అర్హత {e} కిలోలు.",
        "hi": "✅ **वज़न सही है** — तौल {r} किलो, हक़ {e} किलो।",
    },
    "SHORT_WEIGHT": {
        "en": "⚠️ **Short weight** — weighed {r} kg, entitled {e} kg: short by {s} kg.",
        "te": "⚠️ **తక్కువ తూకం** — తూకం {r} కిలోలు, అర్హత {e} కిలోలు: {s} కిలోలు తక్కువ.",
        "hi": "⚠️ **कम तौल** — तौल {r} किलो, हक़ {e} किलो: {s} किलो कम।",
    },
    "NEEDS_REVIEW": {
        "en": ("🔎 **Needs review** — the reading ({r} kg) is far above your entitlement ({e} kg), possibly a misread. "
               "Please retake the photo or type the weight."),
        "te": ("🔎 **పరిశీలన అవసరం** — రీడింగ్ ({r} కిలోలు) మీ అర్హత ({e} కిలోలు) కంటే చాలా ఎక్కువ, తప్పుగా చదివి "
               "ఉండవచ్చు. దయచేసి మళ్లీ ఫోటో తీయండి లేదా బరువు టైప్ చేయండి."),
        "hi": ("🔎 **जाँच ज़रूरी** — रीडिंग ({r} किलो) आपके हक़ ({e} किलो) से बहुत ज़्यादा है, शायद गलत पढ़ी गई। "
               "कृपया फिर से फोटो लें या वज़न लिखें।"),
    },
    "UNREADABLE": {
        "en": ("📷 **Couldn't read the weight** from the photo. Please retake it (scale display clear, no glare) "
               "or type the weight you received."),
        "te": "📷 **ఫోటో నుండి బరువు చదవలేకపోయాం.** స్కేల్ డిస్‌ప్లే స్పష్టంగా కనిపించేలా మళ్లీ ఫోటో తీయండి, లేదా బరువు టైప్ చేయండి.",
        "hi": "📷 **फोटो से वज़न नहीं पढ़ पाए।** तराज़ू का डिस्प्ले साफ़ दिखे ऐसी फोटो फिर से भेजें, या वज़न लिखें।",
    },
    "proof": {
        "en": "Time-stamped proof photo (stored on Cloudinary):",
        "te": "సమయ ముద్రతో ఫోటో రుజువు (Cloudinary లో భద్రం):",
        "hi": "समय-मुहर वाली फोटो (Cloudinary पर सुरक्षित):",
    },
    "manual_note": {
        "en": "_(Based on the weight you typed — attach a scale photo for photo proof.)_",
        "te": "_(మీరు టైప్ చేసిన బరువు ఆధారంగా — రుజువు కోసం స్కేల్ ఫోటో జత చేయండి.)_",
        "hi": "_(आपके लिखे वज़न के आधार पर — सबूत के लिए तराज़ू की फोटो भेजें।)_",
    },
    "confirm_prompt": {
        "en": ("Reply **confirm** to finalise this complaint text, or **cancel** to discard it. "
               "RationSeva never files a complaint on its own."),
        "te": ("ఈ ఫిర్యాదు ఖరారు చేయడానికి **అవును** (confirm), వద్దనుకుంటే **వద్దు** (cancel) అని పంపండి. "
               "రేషన్ సేవ మీ తరఫున ఎప్పుడూ స్వయంగా ఫిర్యాదు చేయదు."),
        "hi": ("इस शिकायत को पक्का करने के लिए **हाँ** (confirm) लिखें, या हटाने के लिए **नहीं** (cancel)। "
               "राशन सेवा कभी खुद शिकायत दर्ज नहीं करती।"),
    },
    "confirmed": {
        "en": ("Confirmed. Here is your final complaint. RationSeva has **not** sent it — please send it yourself "
               "(call the PDS helpline 1967, or submit it at your Mandal office / grievance portal):"),
        "te": ("నిర్ధారించబడింది. మీ తుది ఫిర్యాదు ఇదిగో. రేషన్ సేవ దీన్ని **పంపలేదు** — దయచేసి మీరే పంపండి "
               "(PDS హెల్ప్‌లైన్ 1967 కి కాల్ చేయండి, లేదా మండల కార్యాలయం / ఫిర్యాదుల పోర్టల్‌లో ఇవ్వండి):"),
        "hi": ("पुष्टि हो गई। यह रही आपकी अंतिम शिकायत। राशन सेवा ने इसे **नहीं** भेजा है — कृपया खुद भेजें "
               "(PDS हेल्पलाइन 1967 पर कॉल करें, या मंडल कार्यालय / शिकायत पोर्टल पर दें):"),
    },
    "cancelled": {
        "en": "Okay, the complaint draft was discarded.",
        "te": "సరే, ఫిర్యాదు ముసాయిదా తొలగించబడింది.",
        "hi": "ठीक है, शिकायत का मसौदा हटा दिया गया।",
    },
    "photo_error": {
        "en": "I couldn't open that photo. Please attach it again, or type the weight you received.",
        "te": "ఆ ఫోటో తెరవలేకపోయాం. దయచేసి మళ్లీ జత చేయండి, లేదా మీకు వచ్చిన బరువు టైప్ చేయండి.",
        "hi": "वह फोटो नहीं खुल पाई। कृपया फिर से भेजें, या मिला हुआ वज़न लिखें।",
    },
}


def t(key, lang, **kw):
    entry = T[key]
    text = entry.get(lang) or entry["en"]
    return text.format(**kw) if kw else text


def unit(u, lang):
    return t(u.upper(), lang) if u.upper() in ("KG", "PKT") else u


def qty(x):
    return f"{x:,.0f}" if float(x).is_integer() else f"{x:,.2f}"


def footer(stock, lang):
    return t("footer", lang, source=stock.source or "AP AePDS", time=stock.data_time)


def not_found(fps_id, lang):
    return t("not_found", lang, fps=fps_id, n=rd.shop_count(), time=rd.data_time())


def _alt_block(analysis, name, lang):
    item = rd.display_name(name, lang)
    shops = analysis.alternatives.get(name, [])
    if not shops:
        return t("alt_none", lang, afso=analysis.afso, item=item)
    lines = [t("alt_header", lang, afso=analysis.afso, item=item)]
    lines += [f"   ➜ **{s.fps_id}** — {qty(s.closing)} {unit(s.unit, lang)}"
              for s in shops]
    return "\n".join(lines)


def stock_reply(stock, analysis, lang):
    """Stock check answer: per-item quantities + status, alternatives for LOW/OUT asked items."""
    out = [t("shop_header", lang, fps=stock.fps_id, afso=stock.afso, district=stock.district)]
    if not stock.commodities:
        item = rd.display_name(rd.dataset_names(stock.commodity_requested)[0], lang) \
            if stock.commodity_requested else stock.commodity_requested
        out.append(t("no_item", lang, item=item))
    status = {a.commodity: a for a in analysis.assessments} if analysis else {}
    for c in stock.commodities:
        a = status.get(c.commodity)
        st = a.status if a else c.status
        line = f"• {rd.display_name(c.commodity, lang)}: {qty(c.closing)} {unit(c.unit, lang)} — {t(st, lang)}"
        if st == "LOW" and a:
            line += f" ({t('pct', lang, p=a.percent_left)})"
        out.append(line)
    if analysis:
        for name in analysis.alternatives:
            out += ["", _alt_block(analysis, name, lang)]
        if analysis.alternatives:
            out.append(t("portability", lang))
    elif stock.commodities:
        out += ["", t("analysis_down", lang)]
    out += ["", footer(stock, lang)]
    return "\n".join(out)


def alternatives_reply(stock, analysis, lang):
    """Answer to "where else can I go?"."""
    out = [t("shop_header", lang, fps=stock.fps_id, afso=stock.afso, district=stock.district)]
    if not stock.commodities and stock.commodity_requested:
        item = rd.display_name(rd.dataset_names(stock.commodity_requested)[0], lang)
        out.append(t("no_item", lang, item=item))
        return "\n".join(out + ["", footer(stock, lang)])
    if not analysis.alternatives:
        out.append(t("alt_all_ok", lang, fps=stock.fps_id))
        return "\n".join(out + ["", footer(stock, lang)])
    own = {a.commodity: a for a in analysis.assessments}
    for name in analysis.alternatives:
        a = own[name]
        line = f"• {rd.display_name(name, lang)}: {qty(a.closing)} {unit(a.unit, lang)} — {t(a.status, lang)}"
        if a.status == "LOW":
            line += f" ({t('pct', lang, p=a.percent_left)})"
        out.append(line)
    for name in analysis.alternatives:
        out += ["", _alt_block(analysis, name, lang)]
        if own[name].status == "AVAILABLE":
            out.append(t("alt_own_ok", lang, item=rd.display_name(name, lang), fps=stock.fps_id))
    out += ["", t("portability", lang), "", footer(stock, lang)]
    return "\n".join(out)


def notice_reply(notice, lang):
    lang_name = T["lang_names"].get(lang, T["lang_names"]["en"])[notice.language]
    return "\n".join([
        t("notice_ready", lang, fps=notice.fps_id, lang_name=lang_name),
        "",
        f"![RationSeva stock notice {notice.fps_id}]({notice.url})",
        "",
        f"[{t('notice_link', lang)}]({notice.url})",
        "",
        t("notice_more", lang, time=notice.data_time),
    ])


def weighing_reply(w, lang):
    r = qty(w.reading_kg) if w.reading_kg is not None else "?"
    verdict = w.verdict if w.verdict in T else "UNREADABLE"
    out = [t(verdict, lang, r=r, e=qty(w.expected_kg), s=qty(w.short_by_kg or 0))]
    if w.proof_url:
        out += ["", t("proof", lang), f"![scale photo]({w.proof_url})", w.proof_url]
    if not w.ocr_used:
        out.append(t("manual_note", lang))
    if w.complaint_draft:
        out += ["", "```", w.complaint_draft, "```", t("confirm_prompt", lang)]
    return "\n".join(out)
