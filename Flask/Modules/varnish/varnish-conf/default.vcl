#
# This a VCL file for Varnish.
#
# See the VCL chapters in the Users Guide at https://www.varnish-cache.org/docs/
# and https://www.varnish-cache.org/trac/wiki/VCLExamples for more examples.

# Marker to tell the VCL compiler that this VCL has been adapted to the
# new 4.0 format.
vcl 4.0;

# Default backend definition. Set this to point to your content server.
backend default {
    .host = "$#ip-proxy#$";
    .port = "$#varnish-port#$";
}

# Allow purge only from the Nifi cluster nodes
acl purge_acl {
    "localhost";
    "servicemap";
}

sub vcl_recv {
    if (req.method == "PRI") {
        /* This will never happen in properly formed traffic (see: RFC7540) */
        return (synth(405));
    }

    if (!req.http.host && req.esi_level == 0 && req.proto ~ "^(?i)HTTP/1.1") {
        /* In HTTP/1.1, Host is required. */
        return (synth(400));
    }

    if (req.method == "PURGE" || req.method == "BAN" ){
        if(client.ip !~ purge_acl ){
            return( synth(405, "Method Not Allowed!") );
        }

        set req.http.X-Ban-Path = regsub( req.url , "\?.*$" , "" );
        set req.http.X-Ban-serviceUri = regsub(
            req.url,
            "(.*[?&]serviceUri=)([^&]*)(&.*)?",
            "\2"
        );

        if( req.http.X-Ban-serviceUri == req.url ){
            return( synth( 400 , "No ban performed. No serviceUri in the query string." ) );
        }

        set req.http.X-Ban-Path-Escaped = regsuball( req.http.X-Ban-Path , "([]{}()|^$.*+?\\/])" , "\\\1" );
        set req.http.X-Ban-serviceUri-Escaped = regsuball( req.http.X-Ban-serviceUri , "([]{}()|^$.*+?\\/])" , "\\\1" );

        set req.http.X-Ban-VQL = "req.url ~ ^" + req.http.X-Ban-Path-Escaped +
                                 "\?.*serviceUri=" + req.http.X-Ban-serviceUri-Escaped +
                                 ".*$";
        ban( req.http.X-Ban-VQL );

        return( synth( 200 , "Ban issued for serviceUri=" + req.http.X-Ban-serviceUri ) );
    }

    if (req.method != "GET" && req.method != "HEAD" &&
        req.method != "PUT" && req.method != "POST" &&
        req.method != "TRACE" && req.method != "OPTIONS" &&
        req.method != "DELETE" && req.method != "PATCH") {
        /* Non-RFC2616 or CONNECT which is weird. */
        return (pipe);
    }

    if (req.method != "GET" && req.method != "HEAD") {
        /* We only deal with GET and HEAD by default */
        return (pass);
    }

    # if (req.http.Cookie) {
    #   /* Not cacheable by default */
    #   return (pass);
    # }

    # if (req.url ~ "^/ownership-api") {
    #   set req.backend_hint = ownership;
    # } else {
    #   set req.backend_hint = default;
    # }

    return (hash);
}


sub vcl_backend_response {
    # Happens after we have read the response headers from the backend.
    #
    # Here you clean the response headers, removing silly Set-Cookie headers
    # and other mistakes your backend does.


    if( !beresp.http.Vary || !(beresp.http.Vary=="Authorization")){
        set beresp.http.Vary = "Authorization";
    }

    if( beresp.http.Cache-Control ){
        unset beresp.http.Cache-Control;
    }

    if( beresp.http.Expires ){
        unset beresp.http.Expires;
    }

    if( beresp.status == 400 || beresp.status == 401 || beresp.status == 404 || beresp.status == 500 ){
        # Do not cache bad responses from the backend
        set beresp.uncacheable = true;
    }else{
        # Good response form the backend
        unset beresp.http.set-cookie;
        set beresp.ttl = 1800s;
    }
}

sub vcl_deliver {
    # Happens when we have all the pieces we need, and are about to send the
    # response to the client.
    #
    # You can do accounting or modifying the final object here.
}