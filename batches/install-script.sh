#!/bin/bash

#*******************************************************************#
# 	install-script.sh								v0.1			#
#-------------------------------------------------------------------#
#	Version	|	Date	|	Author	|			Comments			#			
#-------------------------------------------------------------------#
#		0.1	| 20151018	|	XCN		|								#	
#-------------------------------------------------------------------#
#			| 			|			|								#	
#-------------------------------------------------------------------#
#			| 			|			|								#	
#-------------------------------------------------------------------#
#*******************************************************************#
#	Installation of Java / Tomcat environment 						#
#*******************************************************************#


# Return values #
RET_OK=0
RET_ABORT=64

# ENV Variables  #

TOMCAT_DIR=/opt/tomcat8 export TOMCAT_DIR
JAVA_DIR=/usr/bin export JAVA_DIR

JAVA_EXEC=$JAVA_DIR/java export JAVA_EXEC

# Java Versions
JDK8_PACKAGE=oracle-java8-jdk
JRE8_PACKAGE=oracle-java8-jre
JAVA8INSTALLER_PACKAGE=oracle-java8-installer

JDK7_PACKAGE=oracle-java7-jdk
JRE7_PACKAGE=oracle-java7-jre
JAVA7INSTALLER_PACKAGE=oracle-java7-installer

# Tomcat vars #

TOMCAT_URL=http://wwwftp.ciril.fr/pub/apache/tomcat/tomcat-8/v8.0.28/bin/apache-tomcat-8.0.28.tar.gz



# Java install #


echo "*******************************************************"
echo "*		Java/tomcat install script 						"
echo "*														"
echo "*-----------------------------------------------------"
echo "*												"
echo "*												"
echo "*												"

RES_JAVA8=`dpkg-query -l | grep "$JAVA8INSTALLER_PACKAGE" | wc -l`
RES_JAVA7=`dpkg-query -l | grep "$JAVA7INSTALLER_PACKAGE" | wc -l`
if [ "$RES_JAVA8" -gt 0 ]
	then

	echo "** Java installed !"
	echo `java -version`
	echo "** java packages : `dpkg-query -l | grep "java"`"
elif [ "$RES_JAVA7" -gt 0 ]
	then
	
	echo "** Java installed !"
	echo `java -version`
	echo "** java packages : `dpkg-query -l | grep "java"`"
	
else 
	echo "** $JAVA8INSTALLER_PACKAGE does not exist"
	read -p "** Install Java (y/n) ?" ANS1
	
	case $ANS1 in
	
		y ) 
		
		echo "Which environment ?"
		echo "1- OpenJDK"
		echo "2- Oracle"
		read -p "? " JDK
		
		case JDK in
		
			1 )
			
				echo "** installing OpenJRE"
				sudo apt-get install default-jre
				if [ $? -eq 0 ]
				then
					echo "** installation of default-jre = SUCCES"
					
				else 
					echo "** !!! installation failed. Exiting"
					exit $RET_ABORT
				fi
			
				echo "** now installing OpenJDK"
				sudo apt-get install default-jdk
				if [ $? -eq 0 ]
				then
					echo "** installation of default-jdk = SUCCES"
					
				else 
					echo "** !!! installation failed. Exiting"
					exit $RET_ABORT
				fi
				echo "** Installation of Java finished"
				;;
			2 )
				
				
				echo "** adding repository ppa:webupd8team/java"
				sudo apt-add-repository ppa:webupd8team/java
				
				if [ $? = 0 ]
				then
					echo "** Repo complete !"
				else
					echo "!!! Repo failed !!! return code : $?"
					exit $RET_ABORT
				fi
					
					
				echo "** updating"
				sudo apt-get update
				if [ $? = 0 ]
				then
					echo "** Update complete !"
				else
					echo "!!! Update failed !!! return code : $?"
					exit $RET_ABORT
				fi
					
				echo "** installing oracle-java8-installer"
				sudo apt-get install oracle-java8-installer
				
				if [ $? = 0 ]
				then
					echo "** Install complete !"
				else
					echo "!!! Install failed !!! return code : $?"
					exit $RET_ABORT
				fi
			
			
			;;
		esac
		;;
		
		n )
		
			exit $RET_OK
		;;
		
	esac
	
fi

###### As Java is not installed how could there be a server
read -p "Want to install a server (y/n) ?" ANS2

case $ANS2 in

	y ) 
	
	echo "Which one ?"
	echo "1- Tomcat "
	read -p "? " SERVER

	case $SERVER in 

		1 )
			
			sudo mkdir $TOMCAT_DIR
			sudo chmod 775 -R $TOMCAT_DIR

			cd $TOMCAT_DIR
			wget $TOMCAT_URL
			tar xzf $TOMCAT_DIR/apache-tomcat-8.0.27.tar.gz $TOMCAT_DIR

			if [ $? -eq 0 ]
			then
				rm -f *$TOMCAT_DIR/apache-tomcat-8.0.27.tar.gz
			else
				echo "** !!! Error on untar command"

			fi
			echo "** Tomcat download complete !"

			
			echo "export CATALINA_HOME=\"/opt/tomcat\"" >> ~/.bashrc
			source ~/.bashrc

			echo "Tomcat 8 install complete"
		
		;;
	esac
	;;
esac


