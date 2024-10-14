---
title: 'My Homelab Part 9: Caddy, FileServer and DuckDNS'
updated: 2024-01-29 11:56:31Z
date: 2024-01-23 11:32:33Z
tags: ["homelab"]
---

If you have been following this Homelab series, you probably have several services up and running, and maybe even a homepage linking to all your services.

Up to this point, however, accessing these services outside your home network was not possible, and the services lacked user-friendly, readable domain names. Instead, you had to enter the IP address of your server followed by the port of the service you wanted to access. Wouldn't it be nice if you could access your services like this:
- `https://service1.my_cool_comain.com`
- `https://service2.my_cool_comain.com`
- `https://service3.my_cool_comain.com`

All of this and more can be achieved with a service called a **reverse proxy** combined with a **Domain Name**.

A domain name is the text you type in your browser when you want to access a website. For instance, the domain name to access the Google website is `google.com`. Normally, you would need the IP address of the server hosting the website to access it. It's evident why one would opt for a domain name – it's easier to remember than an IP address and more readable.


There are numerous providers in the market where you can purchase a domain name that you can then use. Additionally, some providers offer domain names for free, with [DuckDNS](https://www.duckdns.org/) being one such provider that I chose to use. It's important to note that when purchasing a domain name, you have more options for customizing how your domain looks. Conversely, when using a free domain provider, you may encounter more limitations.

A reverse proxy is a service that sits in front of your internet connection, and internet traffic passes through it. The reverse proxy can then decide which services to forward the internet traffic to. There are several reasons why one might choose to use a reverse proxy:
- **Security:** Because all internet traffic must pass through the reverse proxy before being forwarded to the services, there is a reduction in the potential attack surface. Rather than focusing on securing all individual services, one only needs to enhance the security of the reverse proxy. 
- **Elimination of Port Numbers:** Even with a domain name for our service, when multiple services run on one server, specifying the port of the service is still necessary for access. If you only access through the domain name, the server won't know which service to forward the traffic to. This issue can be resolved with a reverse proxy.
- **Performance:** A reverse proxy can maintain a cache of static content to reduce the load on internal services, improving overall performance.
- **Load Balancing:** In scenarios where a service is in high demand, and a single server is insufficient to handle all users, multiple servers are needed. A reverse proxy can determine which server to send users to, effectively distributing the load and ensuring optimal performance.

{{< rawhtml >}}
<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:80%" src="/attachments/Untitled%20Diagram.drawio%281%29.png">
    <figcaption style="text-align:center">Exemplary Diagramm of a Reverse Proxy.</figcaption>
</figure>
{{< /rawhtml >}}

There are various reverse proxy options available, such a [nginx](https://www.nginx.com/), [traefik](https://traefik.io/traefik/) and [caddy](https://caddyserver.com/)  to name a few. In my setup, I opted for Caddy for three key reasons:
1. **Default HTTPS Support:** Caddy supports HTTPS by default, eliminating the need to adjust complex settings or deal with certifications to enable HTTPS functionality.
2. **Simplified Configuration:**  Caddy employs a single configuration file with a straightforward syntax to configure the entire service. This simplifies the setup process and makes it more user-friendly.
3. **Integrated File and Web Server:**  Caddy's versatility allows it to function as both a file and web server. This means you can host files from your computer and access them without requiring additional software installation for this specific purpose. 

## Using DuckDNS

To set up DuckDNS, I followed their [official guide](https://www.duckdns.org/install.jsp), which provides instructions on installing DuckDNS on your device.

Utilizing DuckDNS involves two main stages. In the first stage, you create your domain and link it to your server using its external IP. In the second stage, you create a script on your server that will automatically notify DuckDNS when the server's IP changes and update it accordingly.

Here's a brief explanation of how I did it for my Raspberry Pi server:
1. Begin by logging into the  [DuckDNS](https://www.duckdns.org) website. Upon logging in, you should see a page resembling this:

    {{< rawhtml >}}
    <figure>
        <img style="display: block; margin-left: auto; margin-right: auto; width:100%" src="/attachments/5035ba5578f1fafeb04ce7fdcc8d4634.png">
    </figure>
    {{< /rawhtml >}}

2. Enter the desired text for your domain name in the empty field and press the `add domain` button.
3. Ensure that the `current IP` field contains the external IP (not internal IP) of your server.
4. Next, log into your Raspberry Pi using `ssh` (refer to "My Homelab Part 2: DietPi").
5. Create a folder to store all the files:
	```sh
	mkdir duckdns
	cd duckdns
	nano duckdns.sh
	``` 
6. Enter the following line into the `duckdns.sh` script (refer to "My Homelab Part 2: DietPi" for how to use nano) and save the file:
	```sh
	echo url="https://www.duckdns.org/update?domains=exampledomain&token=a7c4d0ad-114e-40ef-ba1d-d217904a50f2&ip=" | curl -k -o ~/duckdns/duck.log -K -
	```
7. Make the script executable:
	```sh
	chmod 700 duck.sh
	```
8. Automate script execution with cron (see "My Homelab Part 0: Prologue" for how cron works):
	```sh
	crontab -e
	```
	Copy and paste the following text, save the file, and close it:
	```sh
	*/5 * * * * ~/duckdns/duck.sh >/dev/null 2>&1
	```
9. Test if the script is working by running it once and checking the log file for an "OK" message:
	```sh
	./duck.sh
	cat duck.log
	``` 
8. Ensure that cron is started as a service:
	```sh
	sudo service cron start
	```

With these steps, your domain name should now point to your server. However, you won't be able to access a service through your domain yet. To achieve that, you'll need to install Caddy and configure the correct port forwarding.

## Installation Caddy

To install Caddy, I followed their [officical installation guide](https://caddyserver.com/docs/install) and  [make caddy a service guide](https://caddyserver.com/docs/running#manual-installation): 

1. Begin by downloading the Caddy binary. Head over to their [download page](https://caddyserver.com/docs/install#static-binaries), choose the appropriate platform (for Raspberry Pi, it should be "Linux arm64"), and select the DuckDNS and Security module. Press download.  

2. Send the downloaded file to your server using `scp`. Ensure you have OpenSSH selected as your SSH server (refer to "My Homelab Part 2: DietPi"). I recommend naming the file `caddy` 

3. Make the file executable and assign yourself as the owner:  
	```sh
	chmod 700 caddy
	chown User_Name caddy
	```  
4. Move Caddy into your ``$PATH$``:
	```sh
	sudo mv caddy /usr/bin/
	```
5. Verify the installation by running the Caddy version command:
	```sh
	caddy version
	```
6. Create a folder for Caddy config files:
	```sh
	mkdir Caddy
	cd Caddy
	touch Caddyfile
	touch caddy.env
	cd ..
	```
7. Create a systemd unit file::
    ```sh
    nano /etc/systemd/system/caddy.service
    ```
8. Enter the following into the file, ensure you choose the correct path for `ExecStart` and `ExecReload` if your configuration file is in a different location:
	```sh
	# caddy.service
	#
	# For using Caddy with a config file.
	#
	# Make sure the ExecStart and ExecReload commands are correct
	# for your installation.
	#
	# See https://caddyserver.com/docs/install for instructions.
	#
	# WARNING: This service does not use the --resume flag, so if you
	# use the API to make changes, they will be overwritten by the
	# Caddyfile next time the service is restarted. If you intend to
	# use Caddy's API to configure it, add the --resume flag to the
	# `caddy run` command or use the caddy-api.service file instead.

	[Unit]
	Description=Caddy
	Documentation=https://caddyserver.com/docs/
	After=network.target network-online.target
	Requires=network-online.target

	[Service]
	Type=notify
	User=caddy
	Group=caddy
	ExecStart=/usr/bin/caddy run --environ --config /root/caddy/Caddyfile --envfile /root/caddy/caddy.env
	ExecReload=/usr/bin/caddy reload --config /root/caddy/Caddyfile --envfile /root/caddy/caddy.env --force
	TimeoutStopSec=5s
	LimitNOFILE=1048576
	LimitNPROC=512
	PrivateTmp=true
	ProtectSystem=full
	AmbientCapabilities=CAP_NET_ADMIN CAP_NET_BIND_SERVICE

	[Install]
	WantedBy=multi-user.target
	```
9. Start Caddy as a service by typing:
	```sh
	sudo systemctl daemon-reload
	sudo systemctl enable --now caddy
	```
10. To verify that it's running, use:
	```sh
	systemctl status caddy
	```
11. Caddy won't work yet as your configuration file is still empty. Check out the next section for configuration details, and then restart Caddy with the following commands:
	```sh
	systemctl stop caddy
	systemctl start caddy
	systemctl status caddy
	```

## Configuration Caddy

All your Caddy configurations will be done in the previously created Caddy folder, which includes two files: the Caddyfile for configurations and the caddy.env file to store environmental variables. If you are unsure about anything or need guidance, refer to the [caddy documentation](https://caddyserver.com/docs/).

Firstly, open the `caddy.env` file and enter the ports for all your running services, along with a name, and the domain. The file should look like this:
```env
DOMAIN=name_of_your_domain.duckdns.org
DUCKDNS_TOKEN=your_duck_dns_token
VAULTWARDEN_PORT=150
HOMEPAGE_PORT=3000
SYNCTHING_PORT=8384
CALIBRE_PORT=8083
UPTIME_PORT=3001
HOME_ASSISTANT_PORT=8123
MQT_PORT=8888
``` 
These variables will be used in the `Caddyfile`. Using variables allows easy modification of ports without changing every occurrence in the `Caddyfile`.

For a simple forwarding from your domain to your homepage, insert the following into the `Caddyfile` :
```
{$DOMAIN} {
    reverse_proxy localhost:{$HOMEPAGE_PORT}
}
```

Save the file and restart Caddy. However, accessing your homepage through your domain won't work yet because you need to port forward and instruct Caddy to use DuckDNS as the domain.


### DuckDNS

Until now, Caddy is aware that it should listen to your domain and forward it to your homepage. However, it won't function without Caddy knowing your DuckDNS token. Therefore, you need to set the token in your `caddy.env` file. To inform Caddy about using the token, add the following to your `Caddyfile`:
```
(tls) {
     tls {
        dns duckdns {$DUCKDNS_TOKEN}
    }
}
```

When you want to utilize the domain on one of your services, you can import it as follows:
```
{$DOMAIN} {
	import tls	
	
	reverse_proxy localhost:{$HOMEPAGE_PORT}
}
```

Caddy will now use your DuckDNS token to request HTTPS certificates from the [Let's Encrypt](https://letsencrypt.org/) server, 
enabling you to access your site through HTTPS via your domain name.

Keep in mind: It may take up to 24 hours for the [Let's Encrypt](https://letsencrypt.org/) server to issue your certificate. Therefore, it might take some time before you can access your website via HTTPS.

### Port Forward

By default, your router is configured to reject all incoming internet traffic for security reasons, preventing unauthorized access to your network. However, this poses a challenge for accessing your hosted services from outside your network. The solution is port forwarding.

Think of a port as a door – port forwarding allows you to open this door and allow internet traffic inside. However, it comes with risks, as malicious actors could also exploit this open door. It is crucial to only open ports that you are confident cannot be misused.

To access services behind your Caddy reverse proxy, you need to port forward ports 80 and 443, responsible for HTTP and HTTPS, respectively. To find out how to port forward with your specific router, search the internet for your router model followed by "How to port forward."

### File Server

Another useful thing that caddy can do is host a fileserver.
A fileserver host a bunch of files making them accessible through the internet.
Because it allows the hosting of static files, it also allows you to host your own website by hosting `.html` files through the same principal.

<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:100%" src="/attachments/c630caf59f1f3fd601872b7b2d7abe63.png">
</figure>

If you want to use a file server you need the following code in your webserver:
```
files.{$DOMAIN} {

   root * /path/towards/files
   file_server browse
}
```
Using "files.{$DOMAIN}" ensures that I will later be able to access my files trhough the use of the following URL: `htpps:///files.your_domain_name`.
The file server of caddy has a bunch of more settings that can be adjusted like compression, root of the files, files to hide and more, to see a full list click [here](https://caddyserver.com/docs/caddyfile/directives/file_server).

### HTTP header

HTTP headers enable the client and server to exchange additional information with an HTTP request or response, contributing to website security. The OWASP [HTTP Headers Cheat Sheet]((https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html)) offers a comprehensive overview of possible headers, and it is advisable to follow their recommendations when setting HTTP header. You can assess the security of your website using [securityheaders.com](https://securityheaders.com/), which evaluates your website's headers and provides a ranking based on them.

HTTP headers let the client and the server pass additional information with an HTTP request or response. 

To set your headers in Caddy, use the following code:
```
(header) {
	header {
		Strict-Transport-Security "max-age=31536000; includeSubdomains"
		X-XSS-Protection "1; mode=block"
		X-Content-Type-Options "nosniff"
		Referrer-Policy "same-origin"
		X-Frame-Options "ALLOW-FROM *.{$DOMAIN}"
		-Server
		Content-Security-Policy "frame-ancestors {$DOMAIN} *.{$DOMAIN}"
		Permissions-Policy "geolocation=(self {$DOMAIN} *.{$DOMAIN}), microphone=()"
        }
}
```

And later when you want to use it you can simply import it like this:
```
{$DOMAIN} {
	import tls
	import header

	reverse_proxy localhost:{$HOMEPAGE_PORT}
}
```

### Adding an Authentication Portal

For this section to work, you need to download Caddy with the Security module selected.

Even though most services have their own authentication methods, adding an extra layer of security with a portal before the user reaches your homepage might be desirable.

<figure>
    <img style="display: block; margin-left: auto; margin-right: auto; width:60%" src="/attachments/Screenshot%20from%202024-01-24%2006-44-08.png">
    <figcaption>Authentication Portal</figcaption>
</figure>

To add the authentication site to Caddy, use the following code:
```
{
    order authenticate before respond
    order authorize before reverse_proxy
    
    security {
    	local identity store localdb {
            realm local
            path /etc/caddy/auth/local/users.json
        }
    	authentication portal myportal {
	    enable identity store localdb
	    cookie domain {$DOMAIN}
	    cookie lifetime 172800 # 48 hours in seconds
	    transform user {
		match email schuppsimon5@gmail.com
		action add role authp/user
	    }
	}  
        authorization policy admin_policy {
           set auth url https://auth.{$DOMAIN}
           allow roles authp/user
       }
    }
}
```
(I got the cookie lifetime never correctly work for me, If someone knows why, shoot me an email)

If you now want to add this security portal to a site of you, you can do the following:
```
{$DOMAIN} {
	import tls
	import header

	authorize with admin_policy
	reverse_proxy localhost:{$HOMEPAGE_PORT}
}
``` 

### Services and Reverse Proxies

Not every service works seamlessly with a reverse proxy. Some may require specific settings or the configuration of the domain name. In such cases, consult the documentation for information on using reverse proxies with the respective service.

It's worth noting that some services may not work at all. For instance, HomeAssistant may pose challenges, and accessing it might be limited to only the home network using an IP address.

## Full Caddyfile

Here's my full Caddyfile for reference:
{{< details "Click here to show it" >}}
```
{
    order authenticate before respond
    order authorize before reverse_proxy
    
    security {
    	local identity store localdb {
            realm local
            path /etc/caddy/auth/local/users.json
        }
    	authentication portal myportal {
	    enable identity store localdb
	    cookie domain {$DOMAIN}
            cookie lifetime 86400 # 24h	    
            cookie samesite lax
            cookie insecure off            

            ui {
                links {
                  "My Identity" "/whoami"
                }
            }
            
            transform user {
		match email schuppsimon5@gmail.com
		action add role authp/user
	    }
	}  
        authorization policy admin_policy {
           set auth url https://auth.{$DOMAIN}
           allow roles authp/user
       }
    }
}

(header) {
	header {
		Strict-Transport-Security "max-age=31536000; includeSubdomains"
		X-XSS-Protection "1; mode=block"
		X-Content-Type-Options "nosniff"
		Referrer-Policy "same-origin"
		X-Frame-Options "ALLOW-FROM *.{$DOMAIN}"
		-Server
		Content-Security-Policy "frame-ancestors {$DOMAIN} *.{$DOMAIN}"
		Permissions-Policy "geolocation=(self {$DOMAIN} *.{$DOMAIN}), microphone=()"
        }
}

(tls) {
     tls {
        dns duckdns {$DUCKDNS_TOKEN}
    }
}

auth.{$DOMAIN} {
    import header
	
    authenticate with myportal
}

{$DOMAIN} {
    import tls
    import header
    
    authorize with admin_policy
    reverse_proxy localhost:{$HOMEPAGE_PORT}
}

vaultwarden.{$DOMAIN} {
    import tls
    # import header
    # i think with the header doesnt work
    
    reverse_proxy localhost:{$VAULTWARDEN_PORT}
}

rss.{$DOMAIN} {
    import tls
    # import header
    # i think with the header doesnt work    

    authorize with admin_policy
    reverse_proxy localhost:{$RSS_PORT}
}

calibre.{$DOMAIN} {
    import tls
    import header
    
    authorize with admin_policy
    reverse_proxy localhost:{$CALIBRE_PORT}
}

uptime.{$DOMAIN} {
    import tls
    import header
    
    authorize with admin_policy
    reverse_proxy localhost:{$UPTIME_PORT}
}

syncthing.{$DOMAIN} {
    import tls
    import header
    
    authorize with admin_policy
    reverse_proxy localhost:{$SYNCTHING_PORT}
}

netdata.{$DOMAIN} {
    import tls
    import header
    
    authorize with admin_policy
    reverse_proxy localhost:{$NETDATA} 
}

media.{$DOMAIN} {
   import tls
   import header

   authorize with admin_policy
   root * /mnt/externalDisk/media
   file_server browse
}

wg.{$DOMAIN} {
   import tls
   import header

   authorize with admin_policy
   reverse_proxy localhost:{$WG_PORT}
}
```
{{< /details >}}


---
References:
- [Blog Post about Authentication Portal](https://blog.sjain.dev/caddy-sso/)
- [Caddy Documentation](https://caddyserver.com/)
- [Security Headers](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html)
