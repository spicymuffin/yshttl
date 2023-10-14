import json

dict = {
    "id": "18b29dd959854b40",
    "threadId": "18b29dd959854b40",
    "labelIds": ["IMPORTANT", "CATEGORY_PERSONAL", "INBOX"],
    "snippet": "",
    "payload": {
        "partId": "",
        "mimeType": "text/plain",
        "filename": "",
        "headers": [
            {"name": "Delivered-To", "value": "yshttl.inbox@gmail.com"},
            {
                "name": "Received",
                "value": "by 2002:a05:6022:73a8:b0:49:1116:52a with SMTP id bl40csp406046lab;        Fri, 13 Oct 2023 09:27:49 -0700 (PDT)",
            },
            {
                "name": "X-Received",
                "value": "by 2002:a81:9149:0:b0:5a7:b782:6dd9 with SMTP id i70-20020a819149000000b005a7b7826dd9mr13263575ywg.26.1697214469178;        Fri, 13 Oct 2023 09:27:49 -0700 (PDT)",
            },
            {
                "name": "ARC-Seal",
                "value": "i=1; a=rsa-sha256; t=1697214469; cv=none;        d=google.com; s=arc-20160816;        b=rNTbmILJcWYQCB2F/SYwYiZUrBnkLnUy4dX0Gy2142BadKmGS4UVDK3kXTwFa5oM2d         jl3yKVgfjm3q5PJZ49JATaOJxBedoQVuXo1DR3NtDY3EHT49ILP+QWwKyPBbcC2qjl+s         iXRKxYlvgYYJheEo9CMomuHF1V0ykngj/GDwWNlCRPsA07mLc98pdved6qy0pKzwL8YJ         X6U4gvU0bchahmljvbTx3ZvebF2hM9rwae7HLnYl1APXpfGjtNBRLY3XxGcUzePR5IWu         sEvXAAykB9f+iz6h4LyAvcEBkX4emaoJ+9hovykpEYBhTTDddsEWoaxALXrxAAfpNqVe         j+JA==",
            },
            {
                "name": "ARC-Message-Signature",
                "value": "i=1; a=rsa-sha256; c=relaxed/relaxed; d=google.com; s=arc-20160816;        h=to:subject:message-id:date:from:mime-version:dkim-signature;        bh=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=;        fh=GY1GQN++TQO5+2ByrxkdJZWcPRHIbaRzazItJ593Ldw=;        b=HJogVuOY9LNw4ch05QYcqgtrk0QWTQcdW3tqi64G/TS0M0z7WACFqcu6zBcfx0PyaU         CkLnCKpboqy+G0BnkeLYPubwbiIenedv29YL5m4y4IuRQ0tz5Z9zIOZZp9RA3dcsSUAH         6Y9IrOEsX/OR7l60oroFG+denRMTowr34PMV97UPICGlozFBBvPuH7oaoRcnKb5FT/PY         wJR3xp9GE2zDfmVG1QUPII8Whg2RXU9i7FZIIlEbnW3/WHbyi6L4tvp1DkfVi5TEl4Wu         XR5i8e+BoMbT/AuWJFUv8tbsVF1C1CzMCmFWZjxnARinsYSyFvE9zigXf8KvV523/nhS         0ZPQ==",
            },
            {
                "name": "ARC-Authentication-Results",
                "value": "i=1; mx.google.com;       dkim=pass header.i=@gmail.com header.s=20230601 header.b=hPCDL7Dc;       spf=pass (google.com: domain of **replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com designates 209.85.220.41 as permitted sender) smtp.mailfrom=**replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com;       dmarc=pass (p=NONE sp=QUARANTINE dis=NONE) header.from=gmail.com",
            },
            {"name": "Return-Path", "value": "<**replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com>"},
            {
                "name": "Received",
                "value": "from mail-sor-f41.google.com (mail-sor-f41.google.com. [209.85.220.41])        by mx.google.com with SMTPS id n125-20020a0dcb83000000b005a7b4ab9d86sor1285311ywd.7.2023.10.13.09.27.49        for <yshttl.inbox@gmail.com>        (Google Transport Security);        Fri, 13 Oct 2023 09:27:49 -0700 (PDT)",
            },
            {
                "name": "Received-SPF",
                "value": "pass (google.com: domain of **replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com designates 209.85.220.41 as permitted sender) client-ip=209.85.220.41;",
            },
            {
                "name": "Authentication-Results",
                "value": "mx.google.com;       dkim=pass header.i=@gmail.com header.s=20230601 header.b=hPCDL7Dc;       spf=pass (google.com: domain of **replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com designates 209.85.220.41 as permitted sender) smtp.mailfrom=**replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com;       dmarc=pass (p=NONE sp=QUARANTINE dis=NONE) header.from=gmail.com",
            },
            {
                "name": "DKIM-Signature",
                "value": "v=1; a=rsa-sha256; c=relaxed/relaxed;        d=gmail.com; s=20230601; t=1697214468; x=1697819268; dara=google.com;        h=to:subject:message-id:date:from:mime-version:from:to:cc:subject         :date:message-id:reply-to;        bh=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=;        b=hPCDL7DcMnbc43XOdAn4RXUKx1cxVLYhlteUznjFESrE01wSV8uIih2PYEp+WaKqR3         AWApmJqtFjZ5rCU2yOXMWpbRQ2IQqv5A388T0uG25akY8Wvd7AwOXwuPva4sj1ajH/CW         ziuJn9tCVguVRC6k7mHGP0AGdmNnx6UgF3nNciU1JzbXXCRgz7VExpICbSdSKBU905Gs         o/o7nFRu2zWET9NwSl2K7wP+IYhJ4bEkbnwo3d8pZdhWT8IP9A4lcs4bu8jIJlXKsiZ+         Oxy2iqUWFj7c1LCagZLmYEWgqJ+UwRhbIZNr1o4eao+aDHLl/HlmXEVj830dyjB//2r+         Wyiw==",
            },
            {
                "name": "X-Google-DKIM-Signature",
                "value": "v=1; a=rsa-sha256; c=relaxed/relaxed;   d=1e100.net; s=20230601; t=1697214468; x=1697819268;        h=to:subject:message-id:date:from:mime-version:x-gm-message-state         :from:to:cc:subject:date:message-id:reply-to;        bh=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=;        b=QLNTD4CTuCzjlkmdxxSptruJNv2/IuIKE9mKEjs42yJkqT5fAfVv6PIkEasvaaTQMn         lo71DC1IzuI1LFHrxjOrW2AAM9+wMZoVfQYMA7uBI1KAEdd4MxaTOToKjr/YHkQhvew9         /Rr6wx5N3B2TS6kaiKry42NZuhMbOehRSFqQyjhXzkIqBRPSxnZRkqHwegMWqzBHlWMb         WCVICzZsFkYGOHBCo2TlxJUkFPK+6meKmfvrZM5xEO0lxeXgz124fjUmTNPBTFQY88J+         dUxyvD1waacKy+7mYbDTg+FeIJqMroRWsx+onin7IJ0jaZSi7WxbJjxzuLCZOTYuoxTo         98+A==",
            },
            {
                "name": "X-Gm-Message-State",
                "value": "AOJu0YwZVR3Fiq2IZ00JwAc72wMAbS/ktkPk3chfQaRP3ZkT18hsQQNs P/rdjAd4vQiS/LJF+sSgrTGKGyRyk/MJVu0GbsU/Nb2dEPKr",
            },
            {
                "name": "X-Google-Smtp-Source",
                "value": "AGHT+IHhIWyZUMtrkNZM2PpsAZTIij68EE4BUOh+B5Vdcg5aRilYT1d7DDXFSs//mZkBR92LhuR2LAHts0H2ctsml58=",
            },
            {
                "name": "X-Received",
                "value": "by 2002:a25:d28f:0:b0:d9a:c79c:828e with SMTP id j137-20020a25d28f000000b00d9ac79c828emr5158516ybg.14.1697214468349; Fri, 13 Oct 2023 09:27:48 -0700 (PDT)",
            },
            {"name": "MIME-Version", "value": "1.0"},
            {"name": "From", "value": "**replaced ALIAS using filter-repo** <**replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com>"},
            {"name": "Date", "value": "Sat, 14 Oct 2023 01:27:36 +0900"},
            {
                "name": "Message-ID",
                "value": "<CADOErdK1Xq-qXSLoHe++yTRFy10tf3T_hK1dNRydZ5cMe6Yz5A@mail.gmail.com>",
            },
            {"name": "Subject", "value": "test1"},
            {"name": "To", "value": "yshttl.inbox@gmail.com"},
            {"name": "Content-Type", "value": 'text/plain; charset="UTF-8"'},
        ],
        "body": {"size": 2, "data": "DQo="},
    },
    "sizeEstimate": 4850,
    "historyId": "1449",
    "internalDate": "1697214456000",
}

dict = {
    "id": "18b29dd959854b40",
    "threadId": "18b29dd959854b40",
    "labelIds": ["IMPORTANT", "CATEGORY_PERSONAL", "INBOX"],
    "snippet": "",
    "payload": {
        "partId": "",
        "mimeType": "text/plain",
        "filename": "",
        "headers": [
            {"name": "Delivered-To", "value": "yshttl.inbox@gmail.com"},
            {
                "name": "Received",
                "value": "by 2002:a05:6022:73a8:b0:49:1116:52a with SMTP id bl40csp406046lab;        Fri, 13 Oct 2023 09:27:49 -0700 (PDT)",
            },
            {
                "name": "X-Received",
                "value": "by 2002:a81:9149:0:b0:5a7:b782:6dd9 with SMTP id i70-20020a819149000000b005a7b7826dd9mr13263575ywg.26.1697214469178;        Fri, 13 Oct 2023 09:27:49 -0700 (PDT)",
            },
            {
                "name": "ARC-Seal",
                "value": "i=1; a=rsa-sha256; t=1697214469; cv=none;        d=google.com; s=arc-20160816;        b=rNTbmILJcWYQCB2F/SYwYiZUrBnkLnUy4dX0Gy2142BadKmGS4UVDK3kXTwFa5oM2d         jl3yKVgfjm3q5PJZ49JATaOJxBedoQVuXo1DR3NtDY3EHT49ILP+QWwKyPBbcC2qjl+s         iXRKxYlvgYYJheEo9CMomuHF1V0ykngj/GDwWNlCRPsA07mLc98pdved6qy0pKzwL8YJ         X6U4gvU0bchahmljvbTx3ZvebF2hM9rwae7HLnYl1APXpfGjtNBRLY3XxGcUzePR5IWu         sEvXAAykB9f+iz6h4LyAvcEBkX4emaoJ+9hovykpEYBhTTDddsEWoaxALXrxAAfpNqVej+JA==",
            },
            {
                "name": "ARC-Message-Signature",
                "value": "i=1; a=rsa-sha256; c=relaxed/relaxed; d=google.com; s=arc-20160816;        h=to:subject:message-id:date:from:mime-version:dkim-signature;        bh=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=;        fh=GY1GQN++TQO5+2ByrxkdJZWcPRHIbaRzazItJ593Ldw=;        b=HJogVuOY9LNw4ch05QYcqgtrk0QWTQcdW3tqi64G/TS0M0z7WACFqcu6zBcfx0PyaU         CkLnCKpboqy+G0BnkeLYPubwbiIenedv29YL5m4y4IuRQ0tz5Z9zIOZZp9RA3dcsSUAH         6Y9IrOEsX/OR7l60oroFG+denRMTowr34PMV97UPICGlozFBBvPuH7oaoRcnKb5FT/PY         wJR3xp9GE2zDfmVG1QUPII8Whg2RXU9i7FZIIlEbnW3/WHbyi6L4tvp1DkfVi5TEl4Wu         XR5i8e+BoMbT/AuWJFUv8tbsVF1C1CzMCmFWZjxnARinsYSyFvE9zigXf8KvV523/nhS         0ZPQ==",
            },
            {
                "name": "ARC-Authentication-Results",
                "value": "i=1; mx.google.com;       dkim=pass header.i=@gmail.com header.s=20230601 header.b=hPCDL7Dc;       spf=pass (google.com: domain of **replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com designates 209.85.220.41 as permitted sender) smtp.mailfrom=**replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com;       dmarc=pass (p=NONE sp=QUARANTINE dis=NONE) header.from=gmail.com",
            },
            {"name": "Return-Path", "value": "<**replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com>"},
            {
                "name": "Received",
                "value": "from mail-sor-f41.google.com (mail-sor-f41.google.com. [209.85.220.41])        by mx.google.com with SMTPS id n125-20020a0dcb83000000b005a7b4ab9d86sor1285311ywd.7.2023.10.13.09.27.49        for <yshttl.inbox@gmail.com>        (Google Transport Security);        Fri, 13 Oct 2023 09:27:49 -0700 (PDT)",
            },
            {
                "name": "Received-SPF",
                "value": "pass (google.com: domain of **replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com designates 209.85.220.41 as permitted sender) client-ip=209.85.220.41;",
            },
            {
                "name": "Authentication-Results",
                "value": "mx.google.com;       dkim=pass header.i=@gmail.com header.s=20230601 header.b=hPCDL7Dc;       spf=pass (google.com: domain of **replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com designates 209.85.220.41 as permitted sender) smtp.mailfrom=**replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com;       dmarc=pass (p=NONE sp=QUARANTINE dis=NONE) header.from=gmail.com",
            },
            {
                "name": "DKIM-Signature",
                "value": "v=1; a=rsa-sha256; c=relaxed/relaxed;        d=gmail.com; s=20230601; t=1697214468; x=1697819268; dara=google.com;        h=to:subject:message-id:date:from:mime-version:from:to:cc:subject         :date:message-id:reply-to;        bh=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=;        b=hPCDL7DcMnbc43XOdAn4RXUKx1cxVLYhlteUznjFESrE01wSV8uIih2PYEp+WaKqR3         AWApmJqtFjZ5rCU2yOXMWpbRQ2IQqv5A388T0uG25akY8Wvd7AwOXwuPva4sj1ajH/CW         ziuJn9tCVguVRC6k7mHGP0AGdmNnx6UgF3nNciU1JzbXXCRgz7VExpICbSdSKBU905Gs         o/o7nFRu2zWET9NwSl2K7wP+IYhJ4bEkbnwo3d8pZdhWT8IP9A4lcs4bu8jIJlXKsiZ+         Oxy2iqUWFj7c1LCagZLmYEWgqJ+UwRhbIZNr1o4eao+aDHLl/HlmXEVj830dyjB//2r+         Wyiw==",
            },
            {
                "name": "X-Google-DKIM-Signature",
                "value": "v=1; a=rsa-sha256; c=relaxed/relaxed;        d=1e100.net; s=20230601; t=1697214468; x=1697819268;        h=to:subject:message-id:date:from:mime-version:x-gm-message-state         :from:to:cc:subject:date:message-id:reply-to;        bh=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=;        b=QLNTD4CTuCzjlkmdxxSptruJNv2/IuIKE9mKEjs42yJkqT5fAfVv6PIkEasvaaTQMn         lo71DC1IzuI1LFHrxjOrW2AAM9+wMZoVfQYMA7uBI1KAEdd4MxaTOToKjr/YHkQhvew9         /Rr6wx5N3B2TS6kaiKry42NZuhMbOehRSFqQyjhXzkIqBRPSxnZRkqHwegMWqzBHlWMb         WCVICzZsFkYGOHBCo2TlxJUkFPK+6meKmfvrZM5xEO0lxeXgz124fjUmTNPBTFQY88J+   dUxyvD1waacKy+7mYbDTg+FeIJqMroRWsx+onin7IJ0jaZSi7WxbJjxzuLCZOTYuoxTo         98+A==",
            },
            {
                "name": "X-Gm-Message-State",
                "value": "AOJu0YwZVR3Fiq2IZ00JwAc72wMAbS/ktkPk3chfQaRP3ZkT18hsQQNs P/rdjAd4vQiS/LJF+sSgrTGKGyRyk/MJVu0GbsU/Nb2dEPKr",
            },
            {
                "name": "X-Google-Smtp-Source",
                "value": "AGHT+IHhIWyZUMtrkNZM2PpsAZTIij68EE4BUOh+B5Vdcg5aRilYT1d7DDXFSs//mZkBR92LhuR2LAHts0H2ctsml58=",
            },
            {
                "name": "X-Received",
                "value": "by 2002:a25:d28f:0:b0:d9a:c79c:828e with SMTP id j137-20020a25d28f000000b00d9ac79c828emr5158516ybg.14.1697214468349; Fri, 13 Oct 2023 09:27:48 -0700 (PDT)",
            },
            {"name": "MIME-Version", "value": "1.0"},
            {"name": "From", "value": "**replaced ALIAS using filter-repo** <**replaced ALIAS using filter-repo****replaced EMAIL using filter-repo**59@gmail.com>"},
            {"name": "Date", "value": "Sat, 14 Oct 2023 01:27:36 +0900"},
            {
                "name": "Message-ID",
                "value": "<CADOErdK1Xq-qXSLoHe++yTRFy10tf3T_hK1dNRydZ5cMe6Yz5A@mail.gmail.com>",
            },
            {"name": "Subject", "value": "test1"},
            {"name": "To", "value": "yshttl.inbox@gmail.com"},
            {"name": "Content-Type", "value": 'text/plain; charset="UTF-8"'},
        ],
        "body": {"size": 2, "data": "DQo="},
    },
    "sizeEstimate": 4850,
    "historyId": "1449",
    "internalDate": "1697214456000",
}

print(json.dumps(dict))