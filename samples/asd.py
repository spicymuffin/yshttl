dict2 = {
    "partId": "",
    "mimeType": "multipart/alternative",
    "filename": "",
    "headers": [
        {"name": "Delivered-To", "value": "yshttl.inbox@gmail.com"},
        {
            "name": "Received",
            "value": "by 2002:a05:6214:714:b0:66d:21a:ccd0 with SMTP id c20csp3850759qvz;        Mon, 16 Oct 2023 08:56:50 -0700 (PDT)",
        },
        {
            "name": "X-Received",
            "value": "by 2002:a25:a044:0:b0:d32:cd49:2469 with SMTP id x62-20020a25a044000000b00d32cd492469mr31443149ybh.24.1697471809892;        Mon, 16 Oct 2023 08:56:49 -0700 (PDT)",
        },
        {
            "name": "ARC-Seal",
            "value": "i=1; a=rsa-sha256; t=1697471809; cv=none;        d=google.com; s=arc-20160816;        b=ohCiRMpWJyutq3M0JSPd2qE9+ckX3/J87VWa1asn5VzhVnOuOyBTnWn3Yfac+Jhj/G         JCEEDnuFevM4JxOs2DQDcFtYC/1u5D78wBPfxYY2JmpE1dj4l6GBg+iqdeVS2JClDTRV         e8sCWeDwZpVTFzFhT6mdyAaMb15c/fWgh67bTzWrvPriusHcqxbwGbj6U6c2leYh9vg1mHeBc95wBI089nDxSagHM75c/UenjYHn3ApWXDTXodxZC0SifL1EP1ITw7OyHJ9AW0nS         CFQE8eRvuWQf3imLMQTfn5oYnzDWD3IaV1oQL6milbk40RV3rJlpSZZa9lPbkODRAEL9         sBCg==",
        },
        {
            "name": "ARC-Message-Signature",
            "value": "i=1; a=rsa-sha256; c=relaxed/relaxed; d=google.com; s=arc-20160816;   h=to:subject:message-id:date:from:mime-version:dkim-signature;        bh=42z8ZRb5ElRBxh8mdhzFzslUYxHPUyTxgIs6Z0J52n0=;        fh=GY1GQN++TQO5+2ByrxkdJZWcPRHIbaRzazItJ593Ldw=;        b=GMmP8/wNnBtif2WKxaX9J9IWZDbi9nGZ/Rq6dLUEB4RA8RKw+lPpSYg2XwM9QgCw+E         SPdRqhVxQUmC9H50/t94xQO1KW7rQg5kLTqZHkLX9j15fuxqdcn3DaPKfWZgEbypUK3/         Qs4ImgYD2Y1kk6RxN63rMPn1HxU1gtpStsWupJJJ5u8NxxAjvWSATp/aCB4onJ6qGzqQ        S/WonqlfTw2D1DteST1ozJxm6bgrHJN3FgJOXIKOrTL78tWD9E/+C1PWZKPf2Khbd4nZ         U+2sC0Y/GTbJgJzQ9OpFIWFCKxUF0gjFTD+8O/+xEx80V44h3222uAzw6UlWrg6xB/CV         KDLw==",
        },
        {
            "name": "ARC-Authentication-Results",
            "value": "i=1; mx.google.com;       dkim=pass header.i=@gmail.com header.s=20230601 header.b=FfpKCai5;       spf=pass (google.com: domain of **replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com designates 209.85.220.41 as permitted sender) smtp.mailfrom=**replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com;       dmarc=pass (p=NONE sp=QUARANTINE dis=NONE) header.from=gmail.com",
        },
        {"name": "Return-Path", "value": "<**replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com>"},
        {
            "name": "Received",
            "value": "from mail-sor-f41.google.com (mail-sor-f41.google.com. [209.85.220.41])        by mx.google.com with SMTPS id 124-20020a251082000000b00d9115ad8962sor2483144ybq.1.2023.10.16.08.56.49        for <yshttl.inbox@gmail.com>        (Google Transport Security);        Mon, 16 Oct 2023 08:56:49 -0700 (PDT)",
        },
        {
            "name": "Received-SPF",
            "value": "pass (google.com: domain of **replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com designates 209.85.220.41 as permitted sender) client-ip=209.85.220.41;",
        },
        {
            "name": "Authentication-Results",
            "value": "mx.google.com;       dkim=pass header.i=@gmail.com header.s=20230601 header.b=FfpKCai5;       spf=pass (google.com: domain of **replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com designates 209.85.220.41 as permitted sender) smtp.mailfrom=**replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com;       dmarc=pass (p=NONE sp=QUARANTINE dis=NONE) header.from=gmail.com",
        },
        {
            "name": "DKIM-Signature",
            "value": "v=1; a=rsa-sha256; c=relaxed/relaxed;        d=gmail.com; s=20230601; t=1697471809; x=1698076609; dara=google.com;        h=to:subject:message-id:date:from:mime-version:from:to:cc:subject         :date:message-id:reply-to;        bh=42z8ZRb5ElRBxh8mdhzFzslUYxHPUyTxgIs6Z0J52n0=;        b=FfpKCai5eTzSYWrYOp5h5ftwZx9Zp8hf1zfwtgV10zL0nFI6egdjiArOU6veJqkzxL         aQzXnIXf17qyPRMODDzGUKVpv8OWVbuqaZkJ2d2x2KXkoyuG/QKCtU5eupFGcTB3QJ3p         kBTXCYspDhxwSLFTqeykZC1HXRY1roOC6urAEcQ2FIT/LqwWSpBMc2EKQcQBfEj1kOJD         Zql1wD/XOeN/O2uyJyuxXajhU7F5qhihDbIwJRNq7wuExd5Qq1a6Fr35fWPOiY8aWUFn         FfWcca5rnMBwKDcveXx1wWvlqjeKjnUgFwHTZznIGzXqFkOKoWHvowl/raMzS02hf5bS         4O5A==",
        },
        {
            "name": "X-Google-DKIM-Signature",
            "value": "v=1; a=rsa-sha256; c=relaxed/relaxed;        d=1e100.net; s=20230601; t=1697471809; x=1698076609;        h=to:subject:message-id:date:from:mime-version:x-gm-message-state         :from:to:cc:subject:date:message-id:reply-to;        bh=42z8ZRb5ElRBxh8mdhzFzslUYxHPUyTxgIs6Z0J52n0=;        b=xN4w2/sydx2Heh5FOgQ6dQmxrmCp9KbGLjgQz3DwfpZkWKcwHZEn3dRWDNys9xkfJK         nvIznnK8utlCeT4D7q7CyLLseuMIVGS9+XZ/JLkhSdrkycrGi6hkhi6nqoSr+m5RW3RO         NYUQVFuLvKwZW4E8YuKsWKQ7AKgc8HLGU8EWLR8eNtcQ5Px5+5WXfBLFN86MgvjhyYH4         LyFB378uNgV0T4K7eYyN2ysFJsj9EBJUP7JWAZDC/XxVkM9LgDaQiQIOOd6WGXUed1pS         XB4I6KiQ6nDTd7G8O/BeBunDb2okmmM16igqECnKrj8dtkFjD/DDzgiA14IqSY4GSMCd         WwoQ==",
        },
        {
            "name": "X-Gm-Message-State",
            "value": "AOJu0YxXxV78E8sStp3nZzmp70tvg6BckNssHOfUgWG0xTxbKiSf/vlj eElGejRgVOuHL5IYvcgyab7BS4NdeE/lIwd5UgQBrEK7TWxC",
        },
        {
            "name": "X-Google-Smtp-Source",
            "value": "AGHT+IHJOzP3DCTUvm7OF8qLsDGV+51Xr+M9268BMs71NXGnG/jEzOiCZ9+U+0a3vsYv8xDZB40AOjBGSJKcFgLAJg4=",
        },
        {
            "name": "X-Received",
            "value": "by 2002:a25:2d15:0:b0:d9a:c4df:cd8e with SMTP id t21-20020a252d15000000b00d9ac4dfcd8emr10568197ybt.33.1697471809227; Mon, 16 Oct 2023 08:56:49 -0700 (PDT)",
        },
        {"name": "MIME-Version", "value": "1.0"},
        {"name": "From", "value": "**replaced ALIAS using filter-repo** <**replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com>"},
        {"name": "Date", "value": "Tue, 17 Oct 2023 00:56:38 +0900"},
        {
            "name": "Message-ID",
            "value": "<CADOErdLLGQWCR7Bd1XteD2smDhCQiro1nGKp6w_o=tb6=f-QOw@mail.gmail.com>",
        },
        {"name": "Subject", "value": "shshaahahhahahahshs"},
        {"name": "To", "value": "yshttl.inbox@gmail.com"},
        {
            "name": "Content-Type",
            "value": 'multipart/alternative; boundary="00000000000034a7350607d774ab"',
        },
    ],
    "body": {"size": 0},
    "parts": [
        {
            "partId": "0",
            "mimeType": "text/plain",
            "filename": "",
            "headers": [
                {"name": "Content-Type", "value": 'text/plain; charset="UTF-8"'}
            ],
            "body": {
                "size": 65,
                "data": "Ym9vaw0KMjAyMzE0ODAwNg0KTHVpZ2lfMjI4IQ0Kb3JpZ2luPXNpbmNob24gZGF0ZT1vdm0gdGltZT0wNzAwDQo=",
            },
        },
        {
            "partId": "1",
            "mimeType": "text/html",
            "filename": "",
            "headers": [
                {"name": "Content-Type", "value": 'text/html; charset="UTF-8"'}
            ],
            "body": {
                "size": 125,
                "data": "Ym9vazxkaXYgZGlyPSJhdXRvIj4yMDIzMTQ4MDA2PC9kaXY-PGRpdiBkaXI9ImF1dG8iPkx1aWdpXzIyOCE8L2Rpdj48ZGl2IGRpcj0iYXV0byI-b3JpZ2luPXNpbmNob24gZGF0ZT1vdm0gdGltZT0wNzAwPC9kaXY-DQo=",
            },
        },
    ],
}

dct3 = {
    "partId": "",
    "mimeType": "text/plain",
    "filename": "",
    "headers": [
        {"name": "Delivered-To", "value": "yshttl.inbox@gmail.com"},
        {
            "name": "Received",
            "value": "by 2002:a05:6214:714:b0:66d:21a:ccd0 with SMTP id c20csp3861048qvz;        Mon, 16 Oct 2023 09:10:15 -0700 (PDT)",
        },
        {
            "name": "X-Received",
            "value": "by 2002:a81:d503:0:b0:59f:65d1:5c55 with SMTP id i3-20020a81d503000000b0059f65d15c55mr37357939ywj.34.1697472615550;        Mon, 16 Oct 2023 09:10:15 -0700 (PDT)",
        },
        {
            "name": "ARC-Seal",
            "value": "i=1; a=rsa-sha256; t=1697472615; cv=none;        d=google.com; s=arc-20160816;        b=UXLbzv0QFAKdHwilPOD0FINkI3Ndjhw/n2l9ueDQq52yFQd35UisgqHF/OEBuGRf/o         mHD7qmBSs6OJgGCjTJ2PpplnRuI/cTdxuz1hUnYS4bskYA90MzWEY5MI565vxGwNGPno         Ib2JEb7Ev9kbUV/mQdOy1rwh99fB8ZpwObBXgAtWoO1/UQAIbt/WXFin9+knToTrLPRq         sfm3AbyqCcIvxJCv46v8riokicVDDGR0JfNcNLdMAJOBih1Te7oY89DzO3nx8h9tvLHk         DX2cIYk6gy9k2PniogeWkmMl8GeV8a+vvBXE7+GeZ9XTpiKMEUXjY1kHwRH6Tt5C0KIO      ez7A==",
        },
        {
            "name": "ARC-Message-Signature",
            "value": "i=1; a=rsa-sha256; c=relaxed/relaxed; d=google.com; s=arc-20160816;        h=to:subject:message-id:date:from:mime-version:dkim-signature;        bh=uYvyue0E+4erhxjdTA2G8dpU9FKgaMKroTWmCrsqJio=;        fh=GY1GQN++TQO5+2ByrxkdJZWcPRHIbaRzazItJ593Ldw=;        b=RIWczGdnZQZ89q9aMFXWsFE1kDLmaLem+KGpArs2XmK5PYIIwtNxzVr2cY0gRaH8+1         yloCzArdzo3aREH7O+Obxd8Ps09PGt/HKqDbcnK51IPdSBEUfNLLoRHdWb4hFF6y4idi         r45Xvs44NEVlWCF4vyVTYUEDc6PybjvrqGQFXUwOedR1mqtDyoOjH4ouO4L2vh5HGEAb         2WawsBoisw7P5N4L2tRAdcZMnwrA0Cx4CCOjWfzOCIIf4C1eMwKyD2sxxlafuOI+HXFS         +9IVpfXmsaKtT8Q69Vr1TrDRSBl4KFsyiujF+0TT8G+Kzrf4vKMzZ8cbtLqPnUF3o/gt     LpKQ==",
        },
        {
            "name": "ARC-Authentication-Results",
            "value": "i=1; mx.google.com;       dkim=pass header.i=@gmail.com header.s=20230601 header.b=crCdcPc5;       spf=pass (google.com: domain of **replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com designates 209.85.220.41 as permitted sender) smtp.mailfrom=**replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com;       dmarc=pass (p=NONE sp=QUARANTINE dis=NONE) header.from=gmail.com",
        },
        {"name": "Return-Path", "value": "<**replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com>"},
        {
            "name": "Received",
            "value": "from mail-sor-f41.google.com (mail-sor-f41.google.com. [209.85.220.41])        by mx.google.com with SMTPS id z68-20020a0dd747000000b005a237b04620sor2361657ywd.9.2023.10.16.09.10.15        for <yshttl.inbox@gmail.com>    (Google Transport Security);        Mon, 16 Oct 2023 09:10:15 -0700 (PDT)",
        },
        {
            "name": "Received-SPF",
            "value": "pass (google.com: domain of **replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com designates 209.85.220.41 as permitted sender) client-ip=209.85.220.41;",
        },
        {
            "name": "Authentication-Results",
            "value": "mx.google.com;       dkim=pass header.i=@gmail.com header.s=20230601 header.b=crCdcPc5;       spf=pass (google.com: domain of **replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com designates 209.85.220.41 as permitted sender) smtp.mailfrom=**replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com;       dmarc=pass (p=NONE sp=QUARANTINE dis=NONE) header.from=gmail.com",
        },
        {
            "name": "DKIM-Signature",
            "value": "v=1; a=rsa-sha256; c=relaxed/relaxed;        d=gmail.com; s=20230601; t=1697472615; x=1698077415; dara=google.com;        h=to:subject:message-id:date:from:mime-version:from:to:cc:subject         :date:message-id:reply-to;        bh=uYvyue0E+4erhxjdTA2G8dpU9FKgaMKroTWmCrsqJio=;        b=crCdcPc51JeXmyOmy3B3ZSA/ywDfMMAUPyM6QcUXxSCe9xyJBT1y7w02pO1NGts0zK         mXSO5HATFhB40Kj9mP/OlEMcMXURM5DOfi/1vAPy9xtdbVPtgO/2f9HQt1lvEpqBGtwu         LUum8OAc1zeyDPtBeZ0ztIrKSPCgxkpow2HtrmOOfK5N17qqopp2dR+tgIlaa2Joi+Rk         liGwY7gVPvBY4kMsHCngY5FVk/cfU12+zF3UEe3PEqBDOSEwFokN9ACh2C+c7qD+n6Mf         GH18PsaFW6W65wKb3cIm1a+LUgL3pKSIUcTjQvxR4dbmMliBo21q1N7MTmJ9M2ZaR/Je         ZrRg==",
        },
        {
            "name": "X-Google-DKIM-Signature",
            "value": "v=1; a=rsa-sha256; c=relaxed/relaxed;        d=1e100.net; s=20230601; t=1697472615; x=1698077415;        h=to:subject:message-id:date:from:mime-version:x-gm-message-state         :from:to:cc:subject:date:message-id:reply-to;        bh=uYvyue0E+4erhxjdTA2G8dpU9FKgaMKroTWmCrsqJio=;        b=HbzL/92elKMnp3V4OsVHGMQwUKE46NlQKFzyaqv9L/3cFfgqssY/rdn/34bYO9tG8e         TAuAOdPSNgNO69gvX6R3ZxcupDo55Q23ffkRXRJHQZ0qd6Cxy1UyVihQeIwqEypk1Vt3         StSbpX9L/t6gi77V+yS5NvX1ZMTCs+lsCtxwrNp7uCjKi7F0K5YT6I9ExCZp9FzWjKcR         l4mNMp/83Rw1rfQ8TdNELE3+YiLODXKQFN9tovG02p26gBMnr8w+71aOjTkeKmCs2gbF         cvUVBEhJCy7lrATihjxsmFzDNX4jvHB4tnJWygm7gdFFl0+wrm5rNmXxHHFoHk4ciXD7         pOIQ==",
        },
        {
            "name": "X-Gm-Message-State",
            "value": "AOJu0YzWgUAq6IbC8hko+iaI6QIc3M/oZP/bAwXTNnOMOxwiVZgfNQdQ GTmAL2ynMXpfS33ctrqQviN2i0wsY4iX+QBoRSkp8IM2IjqCoM4=",
        },
        {
            "name": "X-Google-Smtp-Source",
            "value": "AGHT+IEhs2FhLohqMEsARmUKY2etpVRafKV0H0+v/EIkw1cZbQdScXpF2QfWz/MToCK7rlLQgKJ3mTnfkmSsQYtDNYs=",
        },
        {
            "name": "X-Received",
            "value": "by 2002:a25:b04b:0:b0:d9a:36cc:1c03 with SMTP id e11-20020a25b04b000000b00d9a36cc1c03mr19108562ybj.7.1697472614956; Mon, 16 Oct 2023 09:10:14 -0700 (PDT)",
        },
        {"name": "MIME-Version", "value": "1.0"},
        {"name": "From", "value": "**replaced ALIAS using filter-repo** <**replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com>"},
        {"name": "Date", "value": "Tue, 17 Oct 2023 01:10:02 +0900"},
        {
            "name": "Message-ID",
            "value": "<CADOErdJHm-3Ptq6Ufd1Cx33MjO-RzfC6jAqOOaBb_2epzdqnBg@mail.gmail.com>",
        },
        {"name": "Subject", "value": "asda"},
        {"name": "To", "value": "yshttl.inbox@gmail.com"},
        {"name": "Content-Type", "value": 'text/plain; charset="UTF-8"'},
    ],
    "body": {
        "size": 36,
        "data": "YXNqZGFpamRhancgaA0KYWpkYWtoZHdoDQphc2Rhd2hkYQ0K",
    },
}

dct4 = {
    {
        "partId": "",
        "mimeType": "multipart/alternative",
        "filename": "",
        "headers": [
            {"name": "Delivered-To", "value": "yshttl.inbox@gmail.com"},
            {
                "name": "Received",
                "value": "by 2002:a05:6214:714:b0:66d:21a:ccd0 with SMTP id c20csp3862520qvz;        Mon, 16 Oct 2023 09:12:20 -0700 (PDT)",
            },
            {
                "name": "X-Received",
                "value": "by 2002:a81:9c02:0:b0:585:ef4e:6d93 with SMTP id m2-20020a819c02000000b00585ef4e6d93mr36206396ywa.47.1697472739979;        Mon, 16 Oct 2023 09:12:19 -0700 (PDT)",
            },
            {
                "name": "ARC-Seal",
                "value": "i=1; a=rsa-sha256; t=1697472739; cv=none;        d=google.com; s=arc-20160816;        b=LMEv4BCZh9ZIm8AOJ/jIa1S81fjR7bStrF4XmXlggOqT7xAtQflDZROq4negfCvhBr         5BgJad3hOw2ixLhay923ncAmlIstPABzdmLRXZYWBgkFcEmGnB17i7qFLzXSsn4LoTS5         3UcMGwLTa5mDOa2N6xTyJMAeVdOidnM/+sPmTpcgBPKuFa64vLR8OP76ysUd+U+KvFmW         oT175cKbNIsJycYl7TQ3dUicz3MuXYVHy0WxXMtYmJvgEHb6Nm8NoCVFeGbQc6Iq+Ye2         iX5iIqQRseuHnpsP6QRxzkTc7dyA1Ap700ziVVP6cKX9KNc/wrwubv3ZMlv3brC8ICIz         FLmQ==",
            },
            {
                "name": "ARC-Message-Signature",
                "value": "i=1; a=rsa-sha256; c=relaxed/relaxed; d=google.com; s=arc-20160816;    h=to:subject:message-id:date:from:mime-version:dkim-signature;        bh=UGOOvV682xs9nwVe6xYca9rxDOqWW5MPnnTE1lDohZQ=;        fh=GY1GQN++TQO5+2ByrxkdJZWcPRHIbaRzazItJ593Ldw=;        b=Te+WEOW+c13OALeomgfed5H7mWEXBR1F8JjeKk/kF3De90sZPkc5acPIQHQgWCWbiZ         LmC4Yq/ORe/9pNU8dArHnFIR5X8+NvqY/RUbHeBfHz93tJFqgG43gr0QXhhH3CpjFZv6         bgwLZEY2HHvF2ZOxYL34dDivwt7jWWBTTEkjDkT+147JIRbS1I97KEl453eFKCSnkw5TS8lm9x0U9TLouBjKQkfsXS4rrc7W4Lb4/rfCcHYmU589lPTCj+mG8tkM1j5z/WlXJGpk         Jj8gaRbJXTyQuAcxzxOxzhKrpoyH3XMRu2yz9NK7ATPniEGWOwY6g3DKZGJDgv9bYu/B         m3BA==",
            },
            {
                "name": "ARC-Authentication-Results",
                "value": 'i=1; mx.google.com;       dkim=pass header.i=@gmail.com header.s=20230601 header.b="jphJ/UaR";       spf=pass (google.com: domain of **replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com designates 209.85.220.41 as permitted sender) smtp.mailfrom=**replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com;       dmarc=pass (p=NONE sp=QUARANTINE dis=NONE) header.from=gmail.com',
            },
            {"name": "Return-Path", "value": "<**replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com>"},
            {
                "name": "Received",
                "value": "from mail-sor-f41.google.com (mail-sor-f41.google.com. [209.85.220.41])        by mx.google.com with SMTPS id l22-20020a0de216000000b0059f57f528f5sor2387458ywe.16.2023.10.16.09.12.19        for <yshttl.inbox@gmail.com>        (Google Transport Security);        Mon, 16 Oct 2023 09:12:19 -0700 (PDT)",
            },
            {
                "name": "Received-SPF",
                "value": "pass (google.com: domain of **replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com designates 209.85.220.41 as permitted sender) client-ip=209.85.220.41;",
            },
            {
                "name": "Authentication-Results",
                "value": 'mx.google.com;       dkim=pass header.i=@gmail.com header.s=20230601 header.b="jphJ/UaR";       spf=pass (google.com: domain of **replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com designates 209.85.220.41 as permitted sender) smtp.mailfrom=**replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com;       dmarc=pass (p=NONE sp=QUARANTINE dis=NONE) header.from=gmail.com',
            },
            {
                "name": "DKIM-Signature",
                "value": "v=1; a=rsa-sha256; c=relaxed/relaxed;      d=gmail.com; s=20230601; t=1697472739; x=1698077539; dara=google.com;        h=to:subject:message-id:date:from:mime-version:from:to:cc:subject         :date:message-id:reply-to;        bh=UGOOvV682xs9nwVe6xYca9rxDOqWW5MPnnTE1lDohZQ=;        b=jphJ/UaRMzP0PtiXNcNCEVZGaTmft05bel9AUiQGUB6xxFGzQGy0EulL1wj+f4HdX6         8mGnOYrNLXiyu+B9M+p0l57pEp3H4EwjHUtHEB5RJbc9BQVB9VlzBE3XQGvSCB4f+HPe         8oXMiRSOX/XbBjxiPPvFNkHqq4xSdS/S96B3qirUDydyXrp5ICfMr9B6qV0bMp4p5FmK         JjlloQp7wznjfuMYP+DtsUajh3XoWm99k7G1OQ5FqbPmtwN4FnJIFwNv5vxC8oWoKVy2         B4u6INCV8j0O42bnk6OKoqtKrm/rE4jJDzWcAREm6wv7e6NZoIk75PsbelKmZ9ngqf4L         wBkg==",
            },
            {
                "name": "X-Google-DKIM-Signature",
                "value": "v=1; a=rsa-sha256; c=relaxed/relaxed;        d=1e100.net; s=20230601; t=1697472739; x=1698077539;        h=to:subject:message-id:date:from:mime-version:x-gm-message-state         :from:to:cc:subject:date:message-id:reply-to;        bh=UGOOvV682xs9nwVe6xYca9rxDOqWW5MPnnTE1lDohZQ=;        b=tA68goyLu0OuFwoQD8TIx75y2KM6tnPpjLHJymlIrDC/CGhG8Kw06fA5soNtt+YuwH         v7rd32BfgsQl9iqAlU1A+QslRc1cuYncB6Lp+cS4SXFKXtkX/WhflcbgIbbmp2dPiNvn         +o6OuYO1NQfMj56TaSeMGLYgxZF7elitL+fxOEVyucJNswQGNPdczgWIqHjkaiWv2H+c         M3a/oHlkhxSpyipBahsdFGx5wfN70kmKA/2kuTknQ5g+mjaRL+DmYp+j43QcV2TLxeZq         wOYDqvNgs5k/vN1bgM1UU/LcTttVTsuAXDqRxxNWFy66TSQLITjjoF1uijQLwJMsYhA1         FXJA==",
            },
            {
                "name": "X-Gm-Message-State",
                "value": "AOJu0YxmECyJ/HowjlNAioNg7SX+azW2Rh0jsbNDNkSNMFZDxznMwGb7 Pbvs+RJXo6cFnn0Pt0WE4cVuYZAuJVsg4JhVJLOW7UWSka1j",
            },
            {
                "name": "X-Google-Smtp-Source",
                "value": "AGHT+IHz7AjARhmeY7LvYgoFILMDjxK0nmUz0x4EH0IAFrdXI/Lop4vIiDGtiZiKj4DFIued0pnxxqwqZdVoRVe0/6Y=",
            },
            {
                "name": "X-Received",
                "value": "by 2002:a05:6902:18d3:b0:d9a:e239:a1 with SMTP id ck19-20020a05690218d300b00d9ae23900a1mr13071104ybb.4.1697472739439; Mon, 16 Oct 2023 09:12:19 -0700 (PDT)",
            },
            {"name": "MIME-Version", "value": "1.0"},
            {"name": "From", "value": "**replaced ALIAS using filter-repo** <**replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com>"},
            {"name": "Date", "value": "Tue, 17 Oct 2023 01:12:08 +0900"},
            {
                "name": "Message-ID",
                "value": "<CADOErdLjv4WqVsbPLu4UVVWLO1SmAwEAOj26LYxdCObBCZzRig@mail.gmail.com>",
            },
            {"name": "Subject", "value": "dhshh"},
            {"name": "To", "value": "yshttl.inbox@gmail.com"},
            {
                "name": "Content-Type",
                "value": 'multipart/alternative; boundary="000000000000a6770d0607d7ab38"',
            },
        ],
        "body": {"size": 0},
        "parts": [
            {
                "partId": "0",
                "mimeType": "text/plain",
                "filename": "",
                "headers": [
                    {
                        "name": "Content-Type",
                        "value": 'text/plain; charset="UTF-8"',
                    }
                ],
                "body": {
                    "size": 22,
                    "data": "Ym9vaw0KbG9sDQpsbWFvDQprZWsNCg==",
                },
            },
            {
                "partId": "1",
                "mimeType": "text/html",
                "filename": "",
                "headers": [
                    {
                        "name": "Content-Type",
                        "value": 'text/html; charset="UTF-8"',
                    }
                ],
                "body": {
                    "size": 82,
                    "data": "Ym9vazxkaXYgZGlyPSJhdXRvIj5sb2w8L2Rpdj48ZGl2IGRpcj0iYXV0byI-bG1hbzwvZGl2PjxkaXYgZGlyPSJhdXRvIj5rZWs8L2Rpdj4NCg==",
                },
            },
        ],
    }
}
