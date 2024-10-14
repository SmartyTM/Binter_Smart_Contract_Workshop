<!DOCTYPE html>
<!--[if IE 7]><html lang="en" class="lt-ie10 lt-ie9 lt-ie8"><![endif]-->
<!--[if IE 8]><html lang="en" class="lt-ie10 lt-ie9"> <![endif]-->
<!--[if IE 9]><html lang="en" class="lt-ie10"><![endif]-->
<!--[if gt IE 9]><html lang="en"><![endif]-->
<!--[if !IE]><!--><html lang="en"><!--<![endif]-->
<head>
    <meta charset="UTF-8">

    <script type="text/javascript" nonce="eRa_Onl91GzvfTX9kFDhFA">if (typeof module === 'object') {window.module = module; module = undefined;}</script><style type="text/css" nonce="eRa_Onl91GzvfTX9kFDhFA">
        .bgStyle {
          background-image: none
        }
        .bgStyleIE8 {
          
        }
        .copyright a:focus-visible, 
        .privacy-policy a:focus-visible {
          border-radius: 6px;
          outline: rgb(84, 107, 231) solid 1px;
          outline-offset: 2px;
          text-decoration: none !important;
        }
    </style><title>thoughtmachine - Sign In</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="robots" content="noindex,nofollow" />

    <script type="text/javascript" nonce="eRa_Onl91GzvfTX9kFDhFA">window.cspNonce = 'eRa_Onl91GzvfTX9kFDhFA';</script><script src="https://ok9static.oktacdn.com/assets/js/sdk/okta-signin-widget/7.23.2/js/okta-sign-in.min.js" type="text/javascript" integrity="sha384-OWx+dkAQ72MQYaxS210G706/d1/JLKe2Xp703O+6ovYFqUlT9etGaRo40/Wqoq0I" crossorigin="anonymous"></script>
    <link href="https://ok9static.oktacdn.com/assets/js/sdk/okta-signin-widget/7.23.2/css/okta-sign-in.min.css" type="text/css" rel="stylesheet" integrity="sha384-63aTBe2wMqzMRsDHNmlF/FreSWmf3p08BhUDoPlzVf3d+stbkfWtqmdyJ4He5m3m" crossorigin="anonymous"/>

    <link rel="shortcut icon" href="https://ok9static.oktacdn.com/bc/image/fileStoreRecord?id=fs0fn5kzdyGHwqLvq417" type="image/x-icon"/>
<link href="https://ok9static.oktacdn.com/assets/loginpage/css/loginpage-theme.c8c15f6857642c257bcd94823d968bb1.css" rel="stylesheet" type="text/css"/><link href="/api/internal/brand/theme/style-sheet?touch-point=SIGN_IN_PAGE&v=a24e5aca30c1e697de1380858fe0c59cbf47bd60b25f007506a5d3ea034a3619c50d100af4decfae6dd65645e40b651c" rel="stylesheet" type="text/css">

    <script type="text/javascript" nonce="eRa_Onl91GzvfTX9kFDhFA">
        var okta = {
            locale: 'en',
            deployEnv: 'PROD'
        };
    </script><script nonce="eRa_Onl91GzvfTX9kFDhFA">window.okta || (window.okta = {}); okta.cdnUrlHostname = "//ok9static.oktacdn.com"; okta.cdnPerformCheck = false;</script><script type="text/javascript" nonce="eRa_Onl91GzvfTX9kFDhFA">if (window.module) module = window.module;</script></head>
<body class="auth okta-container">

<!--[if gte IE 8]>
  <![if lte IE 10]>

     <style type="text/css" nonce="eRa_Onl91GzvfTX9kFDhFA">
    .unsupported-browser-banner-wrap {
      padding: 20px;
      border: 1px solid #ddd;
      background-color: #f3fbff;
    }
    .unsupported-browser-banner-inner {
      position: relative;
      width: 735px;
      margin: 0 auto;
      text-align: left;
    }
    .unsupported-browser-banner-inner .icon {
      vertical-align: top;
      margin-right: 20px;
      display: inline-block;
      position: static !important;
    }
    .unsupported-browser-banner-inner a {
      text-decoration: underline;
    }
     </style><div class="unsupported-browser-banner-wrap">
      <div class="unsupported-browser-banner-inner">
        <span class="icon icon-16 icon-only warning-16-yellow"></span>You are using an unsupported browser. For the best experience, update to <a href="//help.okta.com/okta_help.htm?type=oie&locale=en&id=csh-browser-support">a supported browser</a>.</div>
    </div>

  <![endif]>
<![endif]-->
<!--[if IE 8]> <div id="login-bg-image-ie8" class="login-bg-image tb--background bgStyleIE8" data-se="login-bg-image"></div> <![endif]-->
<!--[if (gt IE 8)|!(IE)]><!--> <div id="login-bg-image" class="login-bg-image tb--background bgStyle" data-se="login-bg-image"></div> <!--<![endif]-->

<!-- hidden form for reposting fromURI for X509 auth -->
<form action="/login/cert" method="post" id="x509_login" name="x509_login" class="hide">
    <input type="hidden" id="fromURI" name="fromURI" class="hidden" value="https&#x3a;&#x2f;&#x2f;thoughtmachine.okta.com&#x2f;oauth2&#x2f;default&#x2f;v1&#x2f;authorize&#x3f;client_id&#x3d;0oa3qcdlixHkX2htj417&amp;code_challenge&#x3d;AdCrz3EpzcnAqqXe6ZkLoL6WWF-fITl1kKwY13zS3WQ&amp;code_challenge_method&#x3d;S256&amp;redirect_uri&#x3d;https&#x25;3A&#x25;2F&#x25;2Fdocs.thoughtmachine.net&#x25;2Fauthorization-code&#x25;2Fcallback&amp;response_type&#x3d;code&amp;scope&#x3d;openid&#x2b;profile&#x2b;email&amp;state&#x3d;1c6972d874627761"/>
</form>

<div class="content">
  <div class="applogin-banner">
          <div class="applogin-background"></div>
          <div class="applogin-container">
              <h1>
                  <span class="applogin-app-title">
                    Connecting to</span>
                  <div class="applogin-app-logo">
                      <img src="https://ok9static.oktacdn.com/fs/bco/4/fs03ue8dzk0XC3Xbf417" alt="Docs&#x20;Hub" class="logo oidc_client"/></div>
              </h1>
              <p>Sign in with your account to access Docs Hub</p>
              </div>
      </div>
  <style type="text/css" nonce="eRa_Onl91GzvfTX9kFDhFA">
    .noscript-msg {
        background-color: #fff;
        border-color: #ddd #ddd #d8d8d8;
        box-shadow:0 2px 0 rgba(175, 175, 175, 0.12);
        text-align: center;
        width: 398px;
        min-width: 300px;
        margin: 200px auto;
        border-radius: 3px;
        border-width: 1px;
        border-style: solid;
    }

    .noscript-content {
        padding: 42px;
    }

    .noscript-content h2 {
        padding-bottom: 20px;
    }

    .noscript-content h1 {
        padding-bottom: 25px;
    }

    .noscript-content a {
        background: transparent;
        box-shadow: none;
        display: table-cell;
        vertical-align: middle;
        width: 314px;
        height: 50px;
        line-height: 36px;
        color: #fff;
        background: linear-gradient(#007dc1, #0073b2), #007dc1;
        border: 1px solid;
        border-color: #004b75;
        border-bottom-color: #00456a;
        box-shadow: rgba(0, 0, 0, 0.15) 0 1px 0, rgba(255, 255, 255, 0.1) 0 1px 0 0 inset;
        -webkit-border-radius: 3px;
        border-radius: 3px;
    }

    .noscript-content a:hover {
        background: #007dc1;
        cursor: hand;
        text-decoration: none;
    }
 </style><noscript>
    <div id="noscript-msg" class="noscript-msg">
        <div class="noscript-content">
            <h2>Javascript is required</h2>
            <h1>Javascript is disabled on your browser.&nbspPlease enable Javascript and refresh this page.</h1>
            <a href="." class="tb--button">Refresh</a>
        </div>
    </div>
</noscript>
<div id="signin-container"></div>
  <div id="okta-sign-in" class="auth-container main-container hide">
      <div id="unsupported-onedrive" class="unsupported-message hide">
        <h2 class="o-form-head">Your OneDrive version is not supported</h2>
        <p>Upgrade now by installing the OneDrive for Business Next Generation Sync Client to login to Okta</p>
        <a class="button button-primary tb--button" target="_blank" href="https://support.okta.com/help/articles/Knowledge_Article/Upgrading-to-OneDrive-for-Business-Next-Generation-Sync-Client">
          Learn how to upgrade</a>
      </div>
      <div id="unsupported-cookie" class="unsupported-message hide">
          <h2 class="o-form-head">Cookies are required</h2>
          <p>Cookies are disabled on your browser. Please enable Cookies and refresh this page.</p>
          <a class="button button-primary tb--button" target="_blank" href=".">
              Refresh</a>
      </div>
  </div>
</div>

<div class="footer">
  <div class="footer-container clearfix">
    <p class="copyright">Powered by <a href="https://www.okta.com/?internal_link=wic_login" class="inline-block notranslate">Okta</a></p>
        <p class="privacy-policy"><a href="/privacy" target="_blank" class="inline-block margin-l-10">Privacy Policy</a></p>
    </div>
</div>

<div id="inactive-tab-main-div" class="hide">
    <div class="inactive-tab-container">
    <div class="inactive-tab-header">
        <img src="https://ok9static.oktacdn.com/fs/bco/1/fs03svfsofWz3cYxv417" alt="thoughtmachine" class="report-org-logo"/><div class="divider"></div>
    </div>
    <div class="inactive-tab-content">
        <h2 class="inactive-tab-content-title">The page has timed out</h2>
        <p class="inactive-tab-details">If this page does not reload automatically, please refresh your browser.</p>
    </div>
</div>
</div>
<script nonce="eRa_Onl91GzvfTX9kFDhFA" type="text/javascript">function runLoginPage (fn) {var mainScript = document.createElement('script');mainScript.src = 'https://ok9static.oktacdn.com/assets/js/mvc/loginpage/initLoginPage.pack.58de3be0c9b511a0fdfd7ea4f69b56fc.js';mainScript.crossOrigin = 'anonymous';mainScript.integrity = 'sha384-cJ4LGViZBmIttMPH+ao2RyPuN5BztKWYWIa4smbm56r1cUhkU/Dr6vTS3UoPbKTI';document.getElementsByTagName('head')[0].appendChild(mainScript);fn && mainScript.addEventListener('load', function () { setTimeout(fn, 1) });}</script><script type="text/javascript" nonce="eRa_Onl91GzvfTX9kFDhFA">
(function(){
  var baseUrl = 'https\x3A\x2F\x2Fthoughtmachine.okta.com';
  var suppliedRedirectUri = '';
  var repost = false;
  var stateToken = 'eyJ6aXAiOiJERUYiLCJhbGlhcyI6ImVuY3J5cHRpb25rZXkiLCJ2ZXIiOiIxIiwib2lkIjoiMDBvdDV6em4wY0FSbDZwOHI0MTYiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiZGlyIn0..aPd7QelMQkuWx7c6.C\x2Dk\x2DicFIrHRtrmKgekoPk5\x2D4bx8YIM8ZMgAPEE7fs98g_3owpu6DzOgQvXZCzCl9zPa63efU433QjL9DmaxXZZPc9CxLuM\x2DPwPKBfAaYFsX92_Huws_z5c3rEjMCy4fHM\x2DG_mM51elyI3OrO2YdJkeDGV27yFEurVdzYrHUrdSbvn62Rk8y2\x2DUod92YIIFm9YP0OtoZXuE\x2DEXXLMiGk9BECvuOiQpuLZ5KvmFUx3qwHblcYjEot7ynrp1I0gEUB2UBE8WjAlWJ5yPcqFJ5FjTqTg7hyMUvj7Sy2PUdB0Pz\x2DfSBkN0sL1szxsgf59_qYN_U6WyiNksSTDmTA\x2D6CBu2X0o6JuJU54LCdp5eXJuuYfdGmYLXyZsvWs3k9xjXrfkmkwPNBrQZWHUjEUZ3QowfAgXPvEqA4vf3068PKmP2\x2DXYIzYxWzF7K064eExwTWx6b5HwHVXn9WeeJ79me9JQaM4uidgOdDX\x2Dkaj7yDmga8gOhgX0PFeEtYgH2YeuFH5WzHFiLgaj2p9t45G0n\x2D1wmr_7mMxO9r5LWAF_yP4UEDm8GlcDpJwFpFneASj9\x2D700_IWPINfYyBkxDvB0_KkF29EcuW9NFXnxSwf7iwbSqS79fb9rEAQ8ALnvPEdvazYqJBgyHVleBKTMQk8Y\x2DWUyNL4mFI3tKqBDIazW4VsP3\x2DuMdmblOTQh4pRtbPeAqjNan3TCs7\x2DGvmIxbtJPkMbUiqk8pC_as\x2DHlXZRFwE2JwwY5boX1S458GDf\x2D47685Byn7da_1SpKZPccw970D8Q6lfRLLdYICm6NaGCEDqB244IUNluvGzEB\x2DdfVbLwbHNdfsnEa1vtoBwwF4xJxaD0e3KrJdTYuE8\x2DdmsTYRJ57pyym4dFSeKQoQynh_3ivYh7CUpztlkocQ5DZXVDaKN99Y6I7ZbRQTKBgpqi2awtalA7MD9LWHqDSydEhqGdvUGioDe23_jKoRwT3IJEKMMiO0ui1rkbmSfC0b1m3KwHhhaB3FOi8q\x2DFm7qFTs5NLVDKd4JrfvvvQcHpML2gPpIp0KCbrXVEGewbn2gcwT1Yc69SxOwCyHBu5JSO7faQCnBMjWaQXf1hp_suwEcnSQvtdDNrgrhJrUFkl7QhYcymzieCxa7RhPycUxXhB1Vc3ZqRchmfZorXqzkghASAfwgiU3MOxsSDp9r4oHgz7YW9s2gR4w4KrKczSReImfqQ_YrnHo_p6\x2D5Jdo8ZuwJfsNjJ6CLAngWA\x2D4LZGqJAXPoxyJCJeVwLWDYU_STRKUfOLX3MUJ5n5p_mSmDd_Ney6K5gxX9kg\x2DmMaMglwDXWxJUGi3XaqfFcmmilnCYKNpsv\x2Dur0Sti5\x2DbUHo03PaudY9Udp_aTg0sVQf\x2DY1uYCr\x2DSmHuSe612ruMQB\x2D7jnUO98KkoqwNYJkBNYRmYl\x2DspsJhV38dkeUalVaK4VtsEJyam5ahdVyDfz80uECEW9L8UIpg6G1xj3ELagHWs8VdBg3jDDGocxe554ZC968\x2DrVNP8KPEMDV1O_V5QTxmVu2SBM0u31LqndN3c9jJ1bTtScsOLYmcvR4ninLRc8G9\x2DteaexmleSXANhi5hSsWXVLo3UknSB2IvzZL5BlTWJyUNnDvVjFbiqUlmnBBKy\x2DW8jZgNOtSDSUroyuq8yABt1oPfMQK7nfosaaf1mDWoPnOdZq656h4WYCiXLLjC5\x2Di7yuHJq7RI6FgRw9fT8ONT38uAXd0rJbDUaSqBBiIy2NZ0JFZckBnslCuoE9jfmN9LqJx28APMZGbmKV8nf6pDYNTk7dG4T4UvITy_ylrn_sXhV4VmYYL0OhlbxDv5dwAtjyVjolHuuI1SEr6TEH6Eom46frzh2aExpQ1MJtwp3n\x2DdNTB2WbyoAObqcS0iQNtQ85Pq4qWYLfqS959ZlfwrOvJ71txRzrdNjdjiFKNf5VhwmAZ4uoN28\x2D4SiQhccLJuHV7fWgep8Dyi3ulNN4szDrTI5L68E9P8lpZaEGZGUTx55e_NqCIQ80KjrJsvEaLxo2OFPTIxFZU3qDO2j1OM7YLt4CldbCPy\x2D3khcJ\x2DndT4mrz9O3nepu2je7LJX7juWqLJhUo_qLHcMjJgjfADnDOTuvwIuJj9a9x2\x2DTNf3_7soaXxHVvcu04jshBu_M\x2Ds3\x2DPmMrCNqnNJIZy6eJcfiV2bwG0vhDh2UsV07\x2Dwko4wSWSQAKER3Tkox3gcUZW7LHPE5yO2ZJoEkWb37Xu7aI4bxC0lJ7QzzoTq_jYNrusqfpT7__Fg\x2D3_5bb6_r6Zxz80yt8NioxDx_DhfCNebAvRIXeQH1rnQpqKo\x2DDDwNU2J_zAeO\x2DcmmihGgCnMlNFePWh4zM77HA__Fa6aBGMLh06lYSig1sJNr7HpqymV_mpMHW1YcPhOFaOqdeYc8nww5oowWEA5eh9dFKEZ9DCGpy4GJ7T_ycnINlk76WdSADuX\x2D_k1T6Qw4w3li8qL\x2D51wZYWTXQ83LIJef8IxLAw3PHSPbY3CcvjCE0S1xUJXINAhztn_wf\x2DSyFR_YocbciYvjudCCGDbxVQ7kM4d0x_wDGbO_fKEJtNBMiQ2ouV1q87BPDcEffvN7RU18eVHHOvNryMwo4q_MugBRGTb50Lz5z_\x2DIHhTXG3AAizT_NtbP0weU\x2DyuZfKwQADFZdIDzUNWoHU8537PUGLmnS\x2Dv9xZbCN0femjbYkpEgE7tuYVhneEFLZPNoZIY481rFHb6VEsVcgKeoUugRdk9NFoZ3kdG6RyAR2b1ONlgxAXD8Wj0GbR5WTYgMHkQssdLAIFizhjLHVQUKP2aEFdH1xGZwXwtZUBUi0oBQVpTcmdtiwTcncZdD11LEhSexe5laTDn_I7Pk7T4cYC2xE2rmlmk_6HCnf7bIZhPEnpFO2u7kdgFmBgD3VKLZFwru_FtFK4OmpDu3MBy9s45KxfUToZWGfiNY39v_9CxyMgGRa8qpLiJG2lmVl0aDtGkQwDi_w_qHdKAuSn1oVJ5NnKs88CzBjnD1Z4bklyo36RG_V0khoDKyxbf3MJGddypqmLZr8FBbV48spDXt\x2DxIPVBhAL5Gh8jIXOJJNt\x2DErooz\x2DruV1FHb0q9Fe1KCTMh65cIMXZTi1uz8pYcDIv\x2DXA1Ig3AZcqKPN27L2b8updXgyXWr4WzMW2I4eRmk5SvKUrsWifDngBfUQlpZ_LsyQdq117v_VZeQPzLq389Kr2Jd5nxDy\x2Dnp1loZVfA94Dz\x2Dy65gCFLjZ43\x2DcvnOuxrsTWRt1G_6vz7YqgsC4S9pJJd5fyQphr4aiuaCa38ZhKI2ZK\x2D5aijruaAZJ4dNVVF35ZEj0cSg3JN2s5qezjHWpbi4fgovlNczcNHnp2hiGQHSQWxgtAyHglLQxJfbaVW5xYu9J82YbmDyk2nRvlqXxwmJ8FlK3L4emPxItRiWkjvy3vJCPEQLHyFS4gqkPeCKu3kg_wbECP0flD8SITl\x2DyBlSLAle71Ox5_zsF9pgjDiTFejAOAjQN8aLprmaOpgOPsTCv5rcYY6e\x2Df6t6Uf0HfuGpHI9dlsEYwK7gltF80Ir95TB\x2DERQCEXvJSdMS3\x2D1izi_LfJl4UFR28JaC9B_NJFiTzJ\x2D7yTkJsoRh9UMu8yIK_dpOjLr8yIrIdwW21EvdTSK\x2DvrJboSNnHBJx1m5lguw.\x2DrE76KbhLL6\x2DegzDxH3FSQ';
  var fromUri = 'https\x3A\x2F\x2Fthoughtmachine.okta.com\x2Foauth2\x2Fdefault\x2Fv1\x2Fauthorize\x3Fclient_id\x3D0oa3qcdlixHkX2htj417\x26code_challenge\x3DAdCrz3EpzcnAqqXe6ZkLoL6WWF\x2DfITl1kKwY13zS3WQ\x26code_challenge_method\x3DS256\x26redirect_uri\x3Dhttps\x253A\x252F\x252Fdocs.thoughtmachine.net\x252Fauthorization\x2Dcode\x252Fcallback\x26response_type\x3Dcode\x26scope\x3Dopenid\x2Bprofile\x2Bemail\x26state\x3D1c6972d874627761';
  var username = '';
  var rememberMe = true;
  var smsRecovery = false;
  var callRecovery = false;
  var emailRecovery = true;
  var usernameLabel = 'Username';
  var usernameInlineLabel = '';
  var passwordLabel = 'Password';
  var passwordInlineLabel = '';
  var signinLabel = 'Sign\x20In';
  var forgotpasswordLabel = 'Forgot\x20password\x3F';
  var unlockaccountLabel = 'Unlock\x20account\x3F';
  var helpLabel = 'Help';
  var orgSupportPhoneNumber = '';
  var hideSignOutForMFA = false;
  var hideBackToSignInForReset = false;
  var footerHelpTitle = 'Need\x20help\x20signing\x20in\x3F';
  var recoveryFlowPlaceholder = 'Email\x20or\x20Username';
  var signOutUrl = '';
  var authScheme = 'OAUTH2';
  var hasPasswordlessPolicy = 'true';
  var INVALID_TOKEN_ERROR_CODE = 'errors.E0000011';

  var securityImage = true;
  
    securityImage = false;
  


  var selfServiceUnlock = false;
  
    selfServiceUnlock = true;
  

  var redirectByFormSubmit = false;
  

  var showPasswordRequirementsAsHtmlList = true;

  var autoPush = false;
  
    autoPush = true;
  

  var accountChooserDiscoveryUrl = 'https://login.okta.com/discovery/iframe.html';

  // In case of custom app login, the uri is already absolute, so we must not attach baseUrl
  var redirectUri;
  if (isAbsoluteUri(fromUri)) {
      redirectUri = fromUri;
  } else {
      redirectUri = baseUrl + fromUri;
  }
  

  var backToSignInLink = '';
  
      backToSignInLink = '';
  

  var customButtons;
  var pivProperties = {};

  

  var customLinks = [];
  
  var factorPageCustomLink = {};
  

  var linkParams;
  

  var proxyIdxResponse;
  

  var stateTokenAllFlows;
  

  var idpDiscovery;
  var idpDiscoveryRequestContext;
  

  var showPasswordToggleOnSignInPage = false;
  var showIdentifier = false;
  
    showPasswordToggleOnSignInPage = true;
    showIdentifier = true;
  

  var hasSkipIdpFactorVerificationButton = false;
  

  var hasOAuth2ConsentFeature = false;
  var consentFunc;
  
    hasOAuth2ConsentFeature = true;
  
    consentFunc = {
      cancel: function() {
        window.location.href='https://thoughtmachine.okta.com/login/step-up/redirect?stateToken=eyJ6aXAiOiJERUYiLCJhbGlhcyI6ImVuY3J5cHRpb25rZXkiLCJ2ZXIiOiIxIiwib2lkIjoiMDBvdDV6em4wY0FSbDZwOHI0MTYiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiZGlyIn0..aPd7QelMQkuWx7c6.C-k-icFIrHRtrmKgekoPk5-4bx8YIM8ZMgAPEE7fs98g_3owpu6DzOgQvXZCzCl9zPa63efU433QjL9DmaxXZZPc9CxLuM-PwPKBfAaYFsX92_Huws_z5c3rEjMCy4fHM-G_mM51elyI3OrO2YdJkeDGV27yFEurVdzYrHUrdSbvn62Rk8y2-Uod92YIIFm9YP0OtoZXuE-EXXLMiGk9BECvuOiQpuLZ5KvmFUx3qwHblcYjEot7ynrp1I0gEUB2UBE8WjAlWJ5yPcqFJ5FjTqTg7hyMUvj7Sy2PUdB0Pz-fSBkN0sL1szxsgf59_qYN_U6WyiNksSTDmTA-6CBu2X0o6JuJU54LCdp5eXJuuYfdGmYLXyZsvWs3k9xjXrfkmkwPNBrQZWHUjEUZ3QowfAgXPvEqA4vf3068PKmP2-XYIzYxWzF7K064eExwTWx6b5HwHVXn9WeeJ79me9JQaM4uidgOdDX-kaj7yDmga8gOhgX0PFeEtYgH2YeuFH5WzHFiLgaj2p9t45G0n-1wmr_7mMxO9r5LWAF_yP4UEDm8GlcDpJwFpFneASj9-700_IWPINfYyBkxDvB0_KkF29EcuW9NFXnxSwf7iwbSqS79fb9rEAQ8ALnvPEdvazYqJBgyHVleBKTMQk8Y-WUyNL4mFI3tKqBDIazW4VsP3-uMdmblOTQh4pRtbPeAqjNan3TCs7-GvmIxbtJPkMbUiqk8pC_as-HlXZRFwE2JwwY5boX1S458GDf-47685Byn7da_1SpKZPccw970D8Q6lfRLLdYICm6NaGCEDqB244IUNluvGzEB-dfVbLwbHNdfsnEa1vtoBwwF4xJxaD0e3KrJdTYuE8-dmsTYRJ57pyym4dFSeKQoQynh_3ivYh7CUpztlkocQ5DZXVDaKN99Y6I7ZbRQTKBgpqi2awtalA7MD9LWHqDSydEhqGdvUGioDe23_jKoRwT3IJEKMMiO0ui1rkbmSfC0b1m3KwHhhaB3FOi8q-Fm7qFTs5NLVDKd4JrfvvvQcHpML2gPpIp0KCbrXVEGewbn2gcwT1Yc69SxOwCyHBu5JSO7faQCnBMjWaQXf1hp_suwEcnSQvtdDNrgrhJrUFkl7QhYcymzieCxa7RhPycUxXhB1Vc3ZqRchmfZorXqzkghASAfwgiU3MOxsSDp9r4oHgz7YW9s2gR4w4KrKczSReImfqQ_YrnHo_p6-5Jdo8ZuwJfsNjJ6CLAngWA-4LZGqJAXPoxyJCJeVwLWDYU_STRKUfOLX3MUJ5n5p_mSmDd_Ney6K5gxX9kg-mMaMglwDXWxJUGi3XaqfFcmmilnCYKNpsv-ur0Sti5-bUHo03PaudY9Udp_aTg0sVQf-Y1uYCr-SmHuSe612ruMQB-7jnUO98KkoqwNYJkBNYRmYl-spsJhV38dkeUalVaK4VtsEJyam5ahdVyDfz80uECEW9L8UIpg6G1xj3ELagHWs8VdBg3jDDGocxe554ZC968-rVNP8KPEMDV1O_V5QTxmVu2SBM0u31LqndN3c9jJ1bTtScsOLYmcvR4ninLRc8G9-teaexmleSXANhi5hSsWXVLo3UknSB2IvzZL5BlTWJyUNnDvVjFbiqUlmnBBKy-W8jZgNOtSDSUroyuq8yABt1oPfMQK7nfosaaf1mDWoPnOdZq656h4WYCiXLLjC5-i7yuHJq7RI6FgRw9fT8ONT38uAXd0rJbDUaSqBBiIy2NZ0JFZckBnslCuoE9jfmN9LqJx28APMZGbmKV8nf6pDYNTk7dG4T4UvITy_ylrn_sXhV4VmYYL0OhlbxDv5dwAtjyVjolHuuI1SEr6TEH6Eom46frzh2aExpQ1MJtwp3n-dNTB2WbyoAObqcS0iQNtQ85Pq4qWYLfqS959ZlfwrOvJ71txRzrdNjdjiFKNf5VhwmAZ4uoN28-4SiQhccLJuHV7fWgep8Dyi3ulNN4szDrTI5L68E9P8lpZaEGZGUTx55e_NqCIQ80KjrJsvEaLxo2OFPTIxFZU3qDO2j1OM7YLt4CldbCPy-3khcJ-ndT4mrz9O3nepu2je7LJX7juWqLJhUo_qLHcMjJgjfADnDOTuvwIuJj9a9x2-TNf3_7soaXxHVvcu04jshBu_M-s3-PmMrCNqnNJIZy6eJcfiV2bwG0vhDh2UsV07-wko4wSWSQAKER3Tkox3gcUZW7LHPE5yO2ZJoEkWb37Xu7aI4bxC0lJ7QzzoTq_jYNrusqfpT7__Fg-3_5bb6_r6Zxz80yt8NioxDx_DhfCNebAvRIXeQH1rnQpqKo-DDwNU2J_zAeO-cmmihGgCnMlNFePWh4zM77HA__Fa6aBGMLh06lYSig1sJNr7HpqymV_mpMHW1YcPhOFaOqdeYc8nww5oowWEA5eh9dFKEZ9DCGpy4GJ7T_ycnINlk76WdSADuX-_k1T6Qw4w3li8qL-51wZYWTXQ83LIJef8IxLAw3PHSPbY3CcvjCE0S1xUJXINAhztn_wf-SyFR_YocbciYvjudCCGDbxVQ7kM4d0x_wDGbO_fKEJtNBMiQ2ouV1q87BPDcEffvN7RU18eVHHOvNryMwo4q_MugBRGTb50Lz5z_-IHhTXG3AAizT_NtbP0weU-yuZfKwQADFZdIDzUNWoHU8537PUGLmnS-v9xZbCN0femjbYkpEgE7tuYVhneEFLZPNoZIY481rFHb6VEsVcgKeoUugRdk9NFoZ3kdG6RyAR2b1ONlgxAXD8Wj0GbR5WTYgMHkQssdLAIFizhjLHVQUKP2aEFdH1xGZwXwtZUBUi0oBQVpTcmdtiwTcncZdD11LEhSexe5laTDn_I7Pk7T4cYC2xE2rmlmk_6HCnf7bIZhPEnpFO2u7kdgFmBgD3VKLZFwru_FtFK4OmpDu3MBy9s45KxfUToZWGfiNY39v_9CxyMgGRa8qpLiJG2lmVl0aDtGkQwDi_w_qHdKAuSn1oVJ5NnKs88CzBjnD1Z4bklyo36RG_V0khoDKyxbf3MJGddypqmLZr8FBbV48spDXt-xIPVBhAL5Gh8jIXOJJNt-Erooz-ruV1FHb0q9Fe1KCTMh65cIMXZTi1uz8pYcDIv-XA1Ig3AZcqKPN27L2b8updXgyXWr4WzMW2I4eRmk5SvKUrsWifDngBfUQlpZ_LsyQdq117v_VZeQPzLq389Kr2Jd5nxDy-np1loZVfA94Dz-y65gCFLjZ43-cvnOuxrsTWRt1G_6vz7YqgsC4S9pJJd5fyQphr4aiuaCa38ZhKI2ZK-5aijruaAZJ4dNVVF35ZEj0cSg3JN2s5qezjHWpbi4fgovlNczcNHnp2hiGQHSQWxgtAyHglLQxJfbaVW5xYu9J82YbmDyk2nRvlqXxwmJ8FlK3L4emPxItRiWkjvy3vJCPEQLHyFS4gqkPeCKu3kg_wbECP0flD8SITl-yBlSLAle71Ox5_zsF9pgjDiTFejAOAjQN8aLprmaOpgOPsTCv5rcYY6e-f6t6Uf0HfuGpHI9dlsEYwK7gltF80Ir95TB-ERQCEXvJSdMS3-1izi_LfJl4UFR28JaC9B_NJFiTzJ-7yTkJsoRh9UMu8yIK_dpOjLr8yIrIdwW21EvdTSK-vrJboSNnHBJx1m5lguw.-rE76KbhLL6-egzDxH3FSQ'
      }
    };
  

  var hasMfaAttestationFeature = false;
  
    hasMfaAttestationFeature = true;
  

  var rememberMyUsernameOnOIE = false;
  
    rememberMyUsernameOnOIE = true;
  

  var engFastpassMultipleAccounts = true;

  var registration = false;
  

  var webauthn = true;
  

    var overrideExistingStateToken = false;
    

  var isPersonalOktaOrg = false;
  

  var sameDeviceOVEnrollmentEnabled = false;
  

  var orgSyncToAccountChooserEnabled = true;
  

  var showSessionRevocation = false;
  
      showSessionRevocation = true;
  

  var hcaptcha;
  

  var loginPageConfig = {
    fromUri: fromUri,
    repost: repost,
    redirectUri: redirectUri,
    backToSignInLink: backToSignInLink,
    isMobileClientLogin: false,
    isMobileSSO: false,
    disableiPadCheck: false,
    enableiPadLoginReload: false,
    linkParams: linkParams,
    hasChromeOSFeature: false,
    showLinkToAppStore: false,
    accountChooserDiscoveryUrl: accountChooserDiscoveryUrl,
    mfaAttestation: hasMfaAttestationFeature,
    isPersonalOktaOrg: isPersonalOktaOrg,
    enrollingFactor: '',
    stateTokenExpiresAt: '',
    stateTokenRefreshWindowMs: '',
    orgSyncToAccountChooserEnabled: orgSyncToAccountChooserEnabled,
    inactiveTab: {
      enabled: true,
      elementId: 'inactive-tab-main-div',
      avoidPageRefresh: true
    },
    signIn: {
      el: '#signin-container',
      baseUrl: baseUrl,
      brandName: 'Okta',
      logo: 'https://ok9static.oktacdn.com/fs/bco/1/fs03svfsofWz3cYxv417',
      logoText: 'thoughtmachine logo',
      helpSupportNumber: orgSupportPhoneNumber,
      stateToken: stateToken,
      username: username,
      signOutLink: signOutUrl,
      consent: consentFunc,
      authScheme: authScheme,
      relayState: fromUri,
      proxyIdxResponse: proxyIdxResponse,
      overrideExistingStateToken: overrideExistingStateToken,
      interstitialBeforeLoginRedirect: 'DEFAULT',
      idpDiscovery: {
        requestContext: idpDiscoveryRequestContext
      },
      features: {
        router: true,
        securityImage: securityImage,
        rememberMe: rememberMe,
        autoPush: autoPush,
        webauthn: webauthn,
        smsRecovery: smsRecovery,
        callRecovery: callRecovery,
        emailRecovery: emailRecovery,
        selfServiceUnlock: selfServiceUnlock,
        multiOptionalFactorEnroll: true,
        sameDeviceOVEnrollmentEnabled: sameDeviceOVEnrollmentEnabled,
        deviceFingerprinting: true,
        useDeviceFingerprintForSecurityImage: true,
        trackTypingPattern: false,
        hideSignOutLinkInMFA: hideSignOutForMFA,
        hideBackToSignInForReset: hideBackToSignInForReset,
        rememberMyUsernameOnOIE: rememberMyUsernameOnOIE,
        engFastpassMultipleAccounts: engFastpassMultipleAccounts,
        customExpiredPassword: true,
        idpDiscovery: idpDiscovery,
        passwordlessAuth: hasPasswordlessPolicy,
        consent: hasOAuth2ConsentFeature,
        skipIdpFactorVerificationBtn: hasSkipIdpFactorVerificationButton,
        showPasswordToggleOnSignInPage: showPasswordToggleOnSignInPage,
        showIdentifier: showIdentifier,
        registration: registration,
        redirectByFormSubmit: redirectByFormSubmit,
        showPasswordRequirementsAsHtmlList: showPasswordRequirementsAsHtmlList,
        showSessionRevocation: showSessionRevocation
      },

      assets: {
        baseUrl: "https\x3A\x2F\x2Fok9static.oktacdn.com\x2Fassets\x2Fjs\x2Fsdk\x2Fokta\x2Dsignin\x2Dwidget\x2F7.23.2"
      },

      language: okta.locale,
      i18n: {},

      customButtons: customButtons,

      piv: pivProperties,

      helpLinks: {
        help: '',
        forgotPassword: '',
        unlock: '',
        custom: customLinks,
        factorPage: factorPageCustomLink
      },

      cspNonce: window.cspNonce,

      hcaptcha: hcaptcha,
    }
  };
  

  loginPageConfig.signIn.i18n[okta.locale] = {
    
    'primaryauth.username.placeholder': usernameLabel,
    'primaryauth.username.tooltip': usernameInlineLabel,
    'primaryauth.password.placeholder': passwordLabel,
    'primaryauth.password.tooltip': passwordInlineLabel,
    'mfa.challenge.password.placeholder': passwordLabel,
    'primaryauth.title': signinLabel,
    'forgotpassword': forgotpasswordLabel,
    'unlockaccount': unlockaccountLabel,
    'help': helpLabel,
    'needhelp': footerHelpTitle,
    'password.forgot.email.or.username.placeholder': recoveryFlowPlaceholder,
    'password.forgot.email.or.username.tooltip': recoveryFlowPlaceholder,
    'account.unlock.email.or.username.placeholder': recoveryFlowPlaceholder,
    'account.unlock.email.or.username.tooltip': recoveryFlowPlaceholder
  };

    
            loginPageConfig.signIn.logoText = 'thoughtmachine logo';
            loginPageConfig.signIn.brandName = 'thoughtmachine';
        

  function isOldWebBrowserControl() {
    // We no longer support IE7. If we see the MSIE 7.0 browser mode, it's a good signal
    // that we're in a windows embedded browser.
    if (navigator.userAgent.indexOf('MSIE 7.0') === -1) {
      return false;
    }

    // Because the userAgent is the same across embedded browsers, we use feature
    // detection to see if we're running on older versions that do not support updating
    // the documentMode via x-ua-compatible.
    return document.all && !window.atob;
  }

  function isAbsoluteUri(uri) {
    var pat = /^https?:\/\//i;
    return pat.test(uri);
  }

  var unsupportedContainer = document.getElementById('okta-sign-in');

  var failIfCookiesDisabled = true;
  

  // Old versions of WebBrowser Controls (specifically, OneDrive) render in IE7 browser
  // mode, with no way to override the documentMode. In this case, inform the user they need
  // to upgrade.
  if (isOldWebBrowserControl()) {
    document.getElementById('unsupported-onedrive').removeAttribute('style');
    unsupportedContainer.removeAttribute('style');
  }
  else if (failIfCookiesDisabled && !navigator.cookieEnabled) {
    document.getElementById('unsupported-cookie').removeAttribute('style');
    unsupportedContainer.removeAttribute('style');
  }
  else {
    unsupportedContainer.parentNode.removeChild(unsupportedContainer);
    runLoginPage(function () {
      var res = OktaLogin.initLoginPage(loginPageConfig);
      
    });
  }
}());
</script><script type="text/javascript" nonce="eRa_Onl91GzvfTX9kFDhFA">
  window.addEventListener('load', function(event) {
    function applyStyle(id, styleDef) {
      if (styleDef) {
        var el = document.getElementById(id);
        if (!el) {
          return;
        }
        el.classList.add(styleDef);
      }
    }
    applyStyle('login-bg-image', 'bgStyle');
    applyStyle('login-bg-image-ie8', 'bgStyleIE8');
  });
</script></body>
</html>
