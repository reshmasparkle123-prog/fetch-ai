# RationSeva — local chat test results (2026-10-30)

Produced by `python scripts/test_chat.py` against all five agents started with `python scripts/run_local.py --no-mailbox`, live backend https://ration-seva.onrender.com (real Cloudinary calls). Scale photo: `scale.png` from the ration-seva repo (display reads 68.5 kg).

Coordinator: `agent1q0gvf0grxdvpqzg4t4s55p5du4y97daurpd99sq40xc8en4qmkrvga9a2fv`

## stock

**USER:** Is rice available at shop 0306122?

**COORDINATOR** (2.8s, end_session=True):

**Shop 0306122** — Ananthagiri AFSO, Alluri Sitharama Raju
• Rice: 9.35 kg — **LOW** (only 0.1% of this month's stock left)

Other shops in Ananthagiri AFSO with Rice available:
   ➜ **0306133** — 2,318.90 kg
   ➜ **0306127** — 1,498.85 kg
   ➜ **0306128** — 1,425.80 kg
With ration-card portability you can collect at another fair-price shop — carry your ration card.

_Data: AP AePDS - Date wise Stock Details (public report), 2026-10-20 22:00 — a dated snapshot, not live. Please confirm at the shop._

## alternatives

**USER:** Rice is low at my shop, where else can I go?

**COORDINATOR** (1.4s, end_session=False):

Which shop? Please send your 7-digit fair-price shop (FPS) number, e.g. 0306122.

**USER:** 0306122

**COORDINATOR** (2.6s, end_session=True):

**Shop 0306122** — Ananthagiri AFSO, Alluri Sitharama Raju
• Rice: 9.35 kg — **LOW** (only 0.1% of this month's stock left)

Other shops in Ananthagiri AFSO with Rice available:
   ➜ **0306133** — 2,318.90 kg
   ➜ **0306127** — 1,498.85 kg
   ➜ **0306128** — 1,425.80 kg

With ration-card portability you can collect at another fair-price shop — carry your ration card.

_Data: AP AePDS - Date wise Stock Details (public report), 2026-10-20 22:00 — a dated snapshot, not live. Please confirm at the shop._

## notice_te

**USER:** Make a Telugu stock notice for 0306122

**COORDINATOR** (2.8s, end_session=True):

Stock notice for shop 0306122 (Telugu) — ready to share on WhatsApp:

![RationSeva stock notice 0306122](https://res.cloudinary.com/imfllew9/image/upload/s--M6Pb2UHV--/c_fill,g_auto,h_1080,w_1080/c_fit,co_rgb:FFD54F,g_north_west,l_text:rationseva:fonts:NotoSansTelugu-Bold.ttf_68:%E0%B0%B0%E0%B1%87%E0%B0%B7%E0%B0%A8%E0%B1%8D%20%E0%B0%B8%E0%B0%B0%E0%B1%81%E0%B0%95%E0%B1%81%E0%B0%B2%E0%B1%81%20%E0%B0%B5%E0%B0%9A%E0%B1%8D%E0%B0%9A%E0%B0%BE%E0%B0%AF%E0%B0%BF,w_920,x_80,y_90/c_fit,co_white,g_north_west,l_text:rationseva:fonts:NotoSansTelugu-Bold.ttf_52:%E0%B0%9A%E0%B0%95%E0%B1%8D%E0%B0%95%E0%B1%86%E0%B0%B0%20%2042%20%E0%B0%95%E0%B0%BF%E0%B0%B2%E0%B1%8B%E0%B0%B2%E0%B1%81,w_920,x_80,y_250/c_fit,co_white,g_north_west,l_text:rationseva:fonts:NotoSansTelugu-Bold.ttf_52:%E0%B0%AC%E0%B0%BF%E0%B0%AF%E0%B1%8D%E0%B0%AF%E0%B0%82%20%209.35%20%E0%B0%95%E0%B0%BF%E0%B0%B2%E0%B1%8B%E0%B0%B2%E0%B1%81,w_920,x_80,y_350/c_fit,co_rgb:FF8A65,g_north_west,l_text:rationseva:fonts:NotoSansTelugu-Bold.ttf_38:%E0%B0%B8%E0%B1%8D%E0%B0%9F%E0%B0%BE%E0%B0%95%E0%B1%8D%20%E0%B0%A4%E0%B0%95%E0%B1%8D%E0%B0%95%E0%B1%81%E0%B0%B5%20-%20%E0%B0%A4%E0%B1%8D%E0%B0%B5%E0%B0%B0%E0%B0%97%E0%B0%BE%20%E0%B0%B0%E0%B0%82%E0%B0%A1%E0%B0%BF,w_920,x_80,y_422/c_fit,co_white,g_north_west,l_text:rationseva:fonts:NotoSansTelugu-Bold.ttf_52:%E0%B0%9A%E0%B0%95%E0%B1%8D%E0%B0%95%E0%B1%86%E0%B0%B0%20%28%E0%B0%85%E0%B0%B0%20%E0%B0%95%E0%B0%BF%E0%B0%B2%E0%B1%8B%29%20%20185%20%E0%B0%AA%E0%B1%8D%E0%B0%AF%E0%B0%BE%E0%B0%95%E0%B1%86%E0%B0%9F%E0%B1%8D%E0%B0%B2%E0%B1%81,w_920,x_80,y_514/c_fit,co_white,g_south_west,l_text:rationseva:fonts:NotoSans-Bold.ttf_40:FPS%200306122,w_920,x_80,y_110/c_fit,co_rgb:DDDDDD,g_south_west,l_text:rationseva:fonts:NotoSans-Regular.ttf_24:As%20per%20AP%20AePDS%20report%252C%2020%20Oct%202026%252C%2010:00%20PM.%20Not%20a%20guarantee%20of%20availability.,w_920,x_80,y_50/f_auto,q_auto/v1/rationseva/notice/base_1080)

[Open / download the image](https://res.cloudinary.com/imfllew9/image/upload/s--M6Pb2UHV--/c_fill,g_auto,h_1080,w_1080/c_fit,co_rgb:FFD54F,g_north_west,l_text:rationseva:fonts:NotoSansTelugu-Bold.ttf_68:%E0%B0%B0%E0%B1%87%E0%B0%B7%E0%B0%A8%E0%B1%8D%20%E0%B0%B8%E0%B0%B0%E0%B1%81%E0%B0%95%E0%B1%81%E0%B0%B2%E0%B1%81%20%E0%B0%B5%E0%B0%9A%E0%B1%8D%E0%B0%9A%E0%B0%BE%E0%B0%AF%E0%B0%BF,w_920,x_80,y_90/c_fit,co_white,g_north_west,l_text:rationseva:fonts:NotoSansTelugu-Bold.ttf_52:%E0%B0%9A%E0%B0%95%E0%B1%8D%E0%B0%95%E0%B1%86%E0%B0%B0%20%2042%20%E0%B0%95%E0%B0%BF%E0%B0%B2%E0%B1%8B%E0%B0%B2%E0%B1%81,w_920,x_80,y_250/c_fit,co_white,g_north_west,l_text:rationseva:fonts:NotoSansTelugu-Bold.ttf_52:%E0%B0%AC%E0%B0%BF%E0%B0%AF%E0%B1%8D%E0%B0%AF%E0%B0%82%20%209.35%20%E0%B0%95%E0%B0%BF%E0%B0%B2%E0%B1%8B%E0%B0%B2%E0%B1%81,w_920,x_80,y_350/c_fit,co_rgb:FF8A65,g_north_west,l_text:rationseva:fonts:NotoSansTelugu-Bold.ttf_38:%E0%B0%B8%E0%B1%8D%E0%B0%9F%E0%B0%BE%E0%B0%95%E0%B1%8D%20%E0%B0%A4%E0%B0%95%E0%B1%8D%E0%B0%95%E0%B1%81%E0%B0%B5%20-%20%E0%B0%A4%E0%B1%8D%E0%B0%B5%E0%B0%B0%E0%B0%97%E0%B0%BE%20%E0%B0%B0%E0%B0%82%E0%B0%A1%E0%B0%BF,w_920,x_80,y_422/c_fit,co_white,g_north_west,l_text:rationseva:fonts:NotoSansTelugu-Bold.ttf_52:%E0%B0%9A%E0%B0%95%E0%B1%8D%E0%B0%95%E0%B1%86%E0%B0%B0%20%28%E0%B0%85%E0%B0%B0%20%E0%B0%95%E0%B0%BF%E0%B0%B2%E0%B1%8B%29%20%20185%20%E0%B0%AA%E0%B1%8D%E0%B0%AF%E0%B0%BE%E0%B0%95%E0%B1%86%E0%B0%9F%E0%B1%8D%E0%B0%B2%E0%B1%81,w_920,x_80,y_514/c_fit,co_white,g_south_west,l_text:rationseva:fonts:NotoSans-Bold.ttf_40:FPS%200306122,w_920,x_80,y_110/c_fit,co_rgb:DDDDDD,g_south_west,l_text:rationseva:fonts:NotoSans-Regular.ttf_24:As%20per%20AP%20AePDS%20report%252C%2020%20Oct%202026%252C%2010:00%20PM.%20Not%20a%20guarantee%20of%20availability.,w_920,x_80,y_50/f_auto,q_auto/v1/rationseva/notice/base_1080)

_Rendered by Cloudinary from the AP AePDS report of 2026-10-20 22:00. Also available in Telugu, Hindi and English — just ask._

## weighing

**USER:** Check my ration weight  _[attached scale.png as URL]_

**COORDINATOR** (1.3s, end_session=False):

📷 Photo received. Please tell me your 7-digit shop number and how many kg you are entitled to (e.g. 20 kg).

**USER:** shop 0306122, entitled 70 kg rice

**COORDINATOR** (6.9s, end_session=False):

⚠️ **Short weight** — weighed 68.50 kg, entitled 70 kg: short by 1.50 kg.

Time-stamped proof photo (stored on Cloudinary):
![scale photo](https://res.cloudinary.com/imfllew9/image/upload/s--1xtD8b6i--/c_limit,w_1280/b_rgb:000000B3,co_white,g_south_west,l_text:Arial_26:30%20Oct%202026%2006:12%20PM%20IST,x_20,y_20/b_rgb:000000B3,co_white,g_south_west,l_text:Arial_34_bold:FPS%200306122%20%7C%20WEIGHING%20PROOF,x_20,y_62/f_auto,q_auto/v1/rationseva/weighing/0306122/20261030_181220)
https://res.cloudinary.com/imfllew9/image/upload/s--1xtD8b6i--/c_limit,w_1280/b_rgb:000000B3,co_white,g_south_west,l_text:Arial_26:30%20Oct%202026%2006:12%20PM%20IST,x_20,y_20/b_rgb:000000B3,co_white,g_south_west,l_text:Arial_34_bold:FPS%200306122%20%7C%20WEIGHING%20PROOF,x_20,y_62/f_auto,q_auto/v1/rationseva/weighing/0306122/20261030_181220

```
COMPLAINT DRAFT (not sent)
To: Civil Supplies Department, Andhra Pradesh (PDS helpline 1967)
Subject: Short weight at fair price shop 0306122

On 2026-10-30, at fair price shop 0306122 (Ananthagiri, Alluri Sitharama Raju), I received Rice weighing 68.5 kg against my entitlement of 70 kg - short by 1.50 kg.
Photo proof (time-stamped, stored by RationSeva on Cloudinary): https://res.cloudinary.com/imfllew9/image/upload/s--1xtD8b6i--/c_limit,w_1280/b_rgb:000000B3,co_white,g_south_west,l_text:Arial_26:30%20Oct%202026%2006:12%20PM%20IST,x_20,y_20/b_rgb:000000B3,co_white,g_south_west,l_text:Arial_34_bold:FPS%200306122%20%7C%20WEIGHING%20PROOF,x_20,y_62/f_auto,q_auto/v1/rationseva/weighing/0306122/20261030_181220
I request an inspection of the shop's weighing scale and the balance quantity.
Name: ______  Ration card no.: ______  Phone: ______
```
Reply **confirm** to finalise this complaint text, or **cancel** to discard it. RationSeva never files a complaint on its own.

**USER:** confirm

**COORDINATOR** (1.3s, end_session=True):

Confirmed. Here is your final complaint. RationSeva has **not** sent it — please send it yourself (call the PDS helpline 1967, or submit it at your Mandal office / grievance portal):

```
To: Civil Supplies Department, Andhra Pradesh (PDS helpline 1967)
Subject: Short weight at fair price shop 0306122

On 2026-10-30, at fair price shop 0306122 (Ananthagiri, Alluri Sitharama Raju), I received Rice weighing 68.5 kg against my entitlement of 70 kg - short by 1.50 kg.
Photo proof (time-stamped, stored by RationSeva on Cloudinary): https://res.cloudinary.com/imfllew9/image/upload/s--1xtD8b6i--/c_limit,w_1280/b_rgb:000000B3,co_white,g_south_west,l_text:Arial_26:30%20Oct%202026%2006:12%20PM%20IST,x_20,y_20/b_rgb:000000B3,co_white,g_south_west,l_text:Arial_34_bold:FPS%200306122%20%7C%20WEIGHING%20PROOF,x_20,y_62/f_auto,q_auto/v1/rationseva/weighing/0306122/20261030_181220
I request an inspection of the shop's weighing scale and the balance quantity.
Name: ______  Ration card no.: ______  Phone: ______
```

## weighing_bytes

**USER:** Check my ration weight at shop 0306122, entitled 65 kg rice  _[attached scale.png as data: URI]_

**COORDINATOR** (6.8s, end_session=True):

✅ **Weight OK** — weighed 68.50 kg, entitled 65 kg.

Time-stamped proof photo (stored on Cloudinary):
![scale photo](https://res.cloudinary.com/imfllew9/image/upload/s--Udu_fdaQ--/c_limit,w_1280/b_rgb:000000B3,co_white,g_south_west,l_text:Arial_26:30%20Oct%202026%2006:12%20PM%20IST,x_20,y_20/b_rgb:000000B3,co_white,g_south_west,l_text:Arial_34_bold:FPS%200306122%20%7C%20WEIGHING%20PROOF,x_20,y_62/f_auto,q_auto/v1/rationseva/weighing/0306122/20261030_181228)
https://res.cloudinary.com/imfllew9/image/upload/s--Udu_fdaQ--/c_limit,w_1280/b_rgb:000000B3,co_white,g_south_west,l_text:Arial_26:30%20Oct%202026%2006:12%20PM%20IST,x_20,y_20/b_rgb:000000B3,co_white,g_south_west,l_text:Arial_34_bold:FPS%200306122%20%7C%20WEIGHING%20PROOF,x_20,y_62/f_auto,q_auto/v1/rationseva/weighing/0306122/20261030_181228

## weighing_no_photo

**USER:** Check my ration weight

**COORDINATOR** (1.3s, end_session=False):

To check your ration weight, attach a photo of the weighing-scale display here, or type the weight you received. Also tell me your shop number and how many kg you are entitled to, e.g. "shop 0306122, entitled 20 kg rice".

**USER:** I got 18 kg instead of 20 kg rice at shop 0306122

**COORDINATOR** (2.0s, end_session=False):

⚠️ **Short weight** — weighed 18 kg, entitled 20 kg: short by 2 kg.
_(Based on the weight you typed — attach a scale photo for photo proof.)_

```
COMPLAINT DRAFT (not sent)
To: Civil Supplies Department, Andhra Pradesh (PDS helpline 1967)
Subject: Short weight at fair price shop 0306122

On 2026-10-30, at fair price shop 0306122 (Ananthagiri, Alluri Sitharama Raju), I received Rice weighing 18 kg against my entitlement of 20 kg - short by 2.00 kg.
Weight as reported by me (no photo).
I request an inspection of the shop's weighing scale and the balance quantity.
Name: ______  Ration card no.: ______  Phone: ______
```
Reply **confirm** to finalise this complaint text, or **cancel** to discard it. RationSeva never files a complaint on its own.

**USER:** cancel

**COORDINATOR** (1.2s, end_session=True):

Okay, the complaint draft was discarded.

## unknown_fps

**USER:** Is rice available at shop 9999999?

**COORDINATOR** (2.0s, end_session=True):

I couldn't find shop **9999999** in our data. We cover the 480 fair-price shops of Alluri Sitharama Raju district (AP AePDS report, 2026-10-20 22:00). Please check the number on your ration card or the shop board.

## telugu_stock

**USER:** 0306122 షాప్‌లో బియ్యం ఉందా?

**COORDINATOR** (2.7s, end_session=True):

**షాప్ 0306122** — Ananthagiri AFSO, Alluri Sitharama Raju
• బియ్యం: 9.35 కిలోలు — **తక్కువగా ఉంది** (ఈ నెల నిల్వలో 0.1% మాత్రమే మిగిలింది)

Ananthagiri AFSO లో బియ్యం అందుబాటులో ఉన్న ఇతర షాపులు:
   ➜ **0306133** — 2,318.90 కిలోలు
   ➜ **0306127** — 1,498.85 కిలోలు
   ➜ **0306128** — 1,425.80 కిలోలు
రేషన్ కార్డు పోర్టబిలిటీతో వేరే రేషన్ షాప్‌లో కూడా సరుకులు తీసుకోవచ్చు — మీ కార్డు తీసుకెళ్లండి.

_సమాచారం: AP AePDS - Date wise Stock Details (public report), 2026-10-20 22:00 — ఇది పాత స్నాప్‌షాట్, లైవ్ కాదు. దయచేసి షాప్ వద్ద నిర్ధారించుకోండి._

## hindi_alternatives

**USER:** मेरी दुकान 0306122 में चावल कम है, और कहाँ मिलेगा?

**COORDINATOR** (2.3s, end_session=True):

**दुकान 0306122** — Ananthagiri AFSO, Alluri Sitharama Raju
• चावल: 9.35 किलो — **कम बचा है** (इस महीने के स्टॉक का केवल 0.1% बचा)

Ananthagiri AFSO में चावल वाली अन्य दुकानें:
   ➜ **0306133** — 2,318.90 किलो
   ➜ **0306127** — 1,498.85 किलो
   ➜ **0306128** — 1,425.80 किलो

राशन कार्ड पोर्टेबिलिटी से आप दूसरी राशन दुकान से भी राशन ले सकते हैं — अपना राशन कार्ड साथ रखें।

_जानकारी: AP AePDS - Date wise Stock Details (public report), 2026-10-20 22:00 — यह पुराना स्नैपशॉट है, लाइव नहीं। कृपया दुकान पर पुष्टि करें।_

## agent_down — Stock Validator stopped

_Ran with `main.py` killed; Coordinator log: `stock validator attempt 1 failed (DeliveryStatus.FAILED: Message delivery failed)`, then attempt 2 the same._

**USER:** Is rice available at shop 0306122?

**COORDINATOR** (8.0s, end_session=True):

Sorry — the stock service is not responding right now. Please try again in a minute.

## notice_te — Notice Agent stopped (fallback to text)

_Ran with `notice_agent.py` killed; Coordinator log: `notice agent attempt 1 failed (DeliveryStatus.FAILED: Message delivery failed)` ×2._

**USER:** Make a Telugu stock notice for 0306122

**COORDINATOR** (9.3s, end_session=True):

Sorry — the notice service is not responding right now. Please try again in a minute.

Here is the stock as text instead:

**Shop 0306122** — Ananthagiri AFSO, Alluri Sitharama Raju
• Sugar: 42 kg — available
• Rice: 9.35 kg — **LOW** (only 0.1% of this month's stock left)
• Sugar (½ kg pkt): 185.35 pkts — available

_Data: AP AePDS - Date wise Stock Details (public report), 2026-10-20 22:00 — a dated snapshot, not live. Please confirm at the shop._
