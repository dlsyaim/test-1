#!/bin/bash


#Check work directory and change into
if [ ! -d /tmp/showins  ]; then
   mkdir -p /tmp/showins
fi
cd /tmp/showins


#Define func nf info check
function nf_check(){

echo > node.txt
echo > temp.txt
echo > amf_id.txt
#echo > udm_addr.txt

# NF count
AMF_C=0
SMF_C=0
#UDM_C=0
#AUSF_C=0
#PCF_C=0
UDR_C=0

# NF show
echo ""
echo "                                       Show all instances of nrf $NRF_ADDR"
echo ""
echo -e "\033[36mUUID\t\t\t\t\t\tNODE_TYPE\tSTATUS\t\t\tADDRESS\t\t\tNODE\033[0m"

curl -X GET "http://$NRF_ADDR:80/nnrf-nfm/v1/nf-instances" 2>/dev/null | python3 -mjson.tool | grep -i nf-instances/ | awk -F '[/\"]' '{print $10}' > line.txt

while read LINE 
do
    curl -X GET "http://$NRF_ADDR:80/nnrf-nfm/v1/nf-instances/$LINE" 2>/dev/null | python3 -m json.tool > temp.txt
    TYPE=$(cat temp.txt | grep -i \"nfType\")
    STATUS=$(cat temp.txt | grep -i \"nfStatus\")
    ADDRESS=$(cat temp.txt | grep -m 1 "[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\{1\}")
    FQDN=$(cat temp.txt | grep -m 1 -i \"fqdn\")
    
    
    TYPE=${TYPE//,/}
    TYPE=${TYPE// /}
    TYPE=${TYPE//\"/}
    TYPE=${TYPE//nfType:/}
    STATUS=${STATUS//,/}
    STATUS=${STATUS// /}
    STATUS=${STATUS//\"/}
    STATUS=${STATUS//nfStatus:/}
    ADDRESS=${ADDRESS//\"fqdn\":\ }
    ADDRESS=${ADDRESS//http:\/\//}
    ADDRESS=${ADDRESS//,/}
    ADDRESS=${ADDRESS// /}
    ADDRESS=${ADDRESS//\"ipv4Address\"\:}
    ADDRESS=${ADDRESS//\"/}
    FQDN=${FQDN// /}
    FQDN=${FQDN//,/}
    FQDN=${FQDN//\"/}
    FQDN=${FQDN//fqdn:/}
    FQDN=${FQDN%%\.*}
    
    
    case $TYPE in
        AMF)
            AMFID=$(cat temp.txt | grep amfId |head -1| cut -d':' -f 2)
            AMFID=${AMFID//\"/}
            echo "$ADDRESS $AMFID" >> amf_id.txt
            AMF_C=$(expr $AMF_C + 1)
            ;;
        SMF)
            SMF_C=$(expr $SMF_C + 1)
            ;;
        UDM)
            UDM_ADDR=$(cat temp.txt | grep -m 1 -i address | cut -d':' -f 2)
            UDM_ADDR=${UDM_ADDR//\"/}
            UDM_ADDR=${UDM_ADDR//,/}
            UDM_ADDR=${UDM_ADDR// /}
#            echo $UDM_ADDR >> udm_addr.txt
#            UDM_C=$(expr $UDM_C + 1)
            ;;
        UDR)
            UDR_C=$(expr $UDR_C + 1)
            ;;
#        PCF)
#            PCF_C=$(expr $PCF_C + 1)
#            ;;
#        AUSF)
#            AUSF_C=$(expr $AUSF_C + 1)
#            ;;
    esac
        
    
    

    if [[ $STATUS =~ "SUSPENDED" ]]; then
        echo -e "\033[7m$LINE\t\t$TYPE\t\t$STATUS\t\t$ADDRESS\t\t$FQDN\033[0m"
    else
        echo -e "$LINE\t\t$TYPE\t\t$STATUS\t\t$ADDRESS\t\t$FQDN"
    fi
    echo -e "$LINE\t\t$TYPE\t\t$STATUS\t\t$ADDRESS\t\t$FQDN" >> node.txt

done < line.txt
echo ""
}



#Define func nf discovery check
function dis_check(){

sed -i '1d' node.txt
sed -i '1d' amf_id.txt
echo -e "\033[36mDiscovery status:\033[0m"

#AMF

while read LINE2
do
    ADDR_X=$(echo $LINE2|cut -d ' ' -f 1)
    ID_X=$(echo $LINE2|cut -d ' ' -f 2)
    curl -s -X GET "http://$NRF_ADDR:80/nnrf-disc/v1/nf-instances?service-names=namf-comm&target-nf-type=AMF&requester-nf-type=SMF&requester-nf-instance-fqdn=njsmf02ber.er.pc.smf.5gc.mnc008.mcc460.3gppnetwork.org&guami=%7B%22plmnId%22%3A%7B%22mcc%22%3A%20%22460%22%2C%20%22mnc%22%3A%20%2208%22%7D%2c%20%22amfId%22%3A%20%22$ID_X%22%7D" > amf.txt
    cat amf.txt | grep -i nfinstanceid > /dev/null
    n_ok "AMF $ADDR_X amf id $ID_X is"
done < amf_id.txt

#SMF
curl -s -X GET "http://$NRF_ADDR:80/nnrf-disc/v1/nf-instances?service-names=nsmf-pdusession&target-nf-type=SMF&requester-nf-type=AMF&dnn=Internet" > smf.txt
SMF_T=$(cat smf.txt | grep -i nfInstanceId | wc -l)
[ $SMF_C == $SMF_T ]  && n_ok "All SMFs are" || n_ok "Not all SMFs are"

#AUSF
curl -s -X GET "http://$NRF_ADDR:80/nnrf-disc/v1/nf-instances?target-nf-type=AUSF&service-names=nausf-auth&requester-nf-type=AMF&supi=imsi-$IMSI" > ausf.txt
cat ausf.txt | grep -i nfinstanceid > /dev/null
n_ok "AUSF is"

#UDM
curl -s -X GET "http://$NRF_ADDR:80/nnrf-disc/v1/nf-instances?target-nf-type=UDM&service-names=nudm-sdm&requester-nf-type=AMF&supi=imsi-$IMSI" > udm.txt
cat udm.txt | grep -i nfinstanceid > /dev/null
n_ok "UDM is"

#PCF
curl -s -X GET "http://$NRF_ADDR:80/nnrf-disc/v1/nf-instances?target-nf-type=PCF&service-names=npcf-am-policy-control&requester-nf-type=AMF&supi=imsi-$IMSI" > pcf.txt
cat pcf.txt | grep -i nfinstanceid > /dev/null
n_ok "PCF is"

#UDR
curl -s -X GET "http://$NRF_ADDR:80/nnrf-disc/v1/nf-instances?target-nf-type=UDR&service-names=nudr-dr&requester-nf-type=UDM&supi=imsi-$IMSI" > udr.txt
UDR_T=$(cat udr.txt | grep -i nfInstanceId | wc -l)
#[ $UDR_C == $UDR_T ]  && n_ok "ALL UDR" || n_ok "NOT ALL UDR"
[ $UDR_T -gt 0 ]  && n_ok "All UDRs are" || n_ok "NOT ALL UDRs are"

echo ""
}


#Define func subscription data check
function scrib_data_check(){
echo -e "\033[36mSubscription data of $IMSI:\033[0m "

curl -m 5 -s -X GET "http://$UDM_ADDR:81/nudm-sdm/v1/imsi-$IMSI/am-data" > am-data.txt
grep -iE "[0-9]{11}" am-data.txt > /dev/null
n_ok "am-data is"
curl -m 5 -s -X GET "http://$UDM_ADDR:81/nudm-sdm/v1/imsi-$IMSI/sm-data" > sm-data.txt
grep -iE "SSC" sm-data.txt > /dev/null
n_ok "sm-data is"
curl -m 5 -s -X GET "http://$UDM_ADDR:81/nudm-sdm/v1/imsi-$IMSI/nssai" > nssai.txt
grep -iE "sst" nssai.txt > /dev/null
n_ok "nssai is"
curl -m 5 -s -X GET "http://$UDM_ADDR:81/nudm-sdm/v1/imsi-$IMSI/smf-select-data" > smf-select-data.txt
grep -i "DnnIndicator" smf-select-data.txt > /dev/null
n_ok "smf-select-data is"
echo ""
}

#print ok or nok
function n_ok(){
if [[ $? == 0 ]];then
    echo $1 OK
else
    echo -e "\033[7m$1 NOK\033[0m"
fi
}

#Define func auth data check
function auth_check(){
SUCI="suci-0-${IMSI:0:3}-${IMSI:3:2}-0000-0-0-${IMSI:5}"
curl -m 5 -s -X POST "http://$UDM_ADDR/nausf-auth/v1/ue-authentications" -H "accept: application/3gppHal+json" -H "Content-Type: application/json" -d "{ \"supiOrSuci\": \"$SUCI\", \"servingNetworkName\": \"5G:mnc008.mcc460.3gppnetwork.org\"}" > auth.txt
cat auth.txt | grep -i 5G_AKA > /dev/null
n_ok "Authen data is"
echo ""

}



# main func
function main(){
    nf_check
    dis_check
    scrib_data_check
    auth_check
}


#Variable evaluation

REGX="^((2(5[0-5]|[0-4][0-9]))|[0-1]?[0-9]{1,2})(\.((2(5[0-5]|[0-4][0-9]))|[0-1]?[0-9]{1,2})){3}$"
UUID="[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"

if [ $# == 2 ];then
    if [[ $2 =~ ^[0-9]{15} ]];then
        if [[ $1 =~ $REGX  ]];then
            IMSI=$2
            NRF_ADDR=$1
            echo "User $IMSI, NRF $NRF_ADDR"
            main
        else
            echo "Address is not regular address"
        fi
    else
        echo "IMSI is not regular IMSI"
    fi
fi


if [ $# == 1 ];then
    NRF_ADDR="10.10.2.34"
    if [[ $1 =~ $UUID ]];then
        curl -X GET "http://$NRF_ADDR:80/nnrf-nfm/v1/nf-instances/$1" 2>/dev/null | python3 -m json.tool
    else
        echo "ID is not regular UUID"
    fi
fi


if [ $# == 0 ];then
    echo "
Usage: ./showins.sh NRF_IP IMSI
Example: ./showins.sh 10.10.2.34 460070000000003
Default NRF 10.10.2.34, user 460070000000003

Alternative usage: ./showins.sh Instance-id
Example: ./showins.sh 1709519d-d124-479a-8ed7-121b0006f86a
"
    NRF_ADDR="10.10.2.34"
    IMSI="460070000000003"
    main
fi



