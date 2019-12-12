
%Matlab script 
%require the matlab abfload addons from https://www.mathworks.com/matlabcentral/fileexchange/22114-fcollman-abfload
% the data obtain in the abf file correspond to deflection in (um) across timeserie


function out = piezoCalibration(path, desiredDeflection)% function name of the function 
% desiredDeflection
% approximate value for the deflection
% low stimulus is 90 ==> output angle should be 2.6
% mid stimulus is 142 ==> output angle should be 4.1
% high stimulus is 200 ==> output angle should be 5.6


%path= 'C:\Users\Windows\Desktop\Tom stim\5p_5hz'
cd(path)

files=dir('*.abf') % list all the abf files in the current directory for one stime type where the input/output curve needs to be done

rstimV=[] % initial the storage of the results for the stim parameter
rpks=[] % initial the storage  of the mean pks obtained
npks=[] % initial the storge of number of pks found

for i=1:length(files) % perform a for loop for all the operation

% extract teh component of the stim parameter based on file name
	str=files(i).name; % extract the file naeme frome the file structure
	stimV = string(extractBetween(str,1,3)); % extract set of string and convert the cell array to string
	rstimV = [rstimV, stimV]; % iteratively store 

% extract the component of the pks parameters
	% work with the data
	data=abfload(files(i).name);% load the abf file
	dSize=size(data); % check the size of the loaded data
	data=data(:,2,:);% the data of interest are IN7 2nd element of s


	if length(dSize)==3
	data=reshape(data, [dSize(1), dSize(3)]); % go from a 3D dimension to 2D array (3D: 1: timeserie, 2: channel, 3: sweeps)
	else
		continue
	end
	data=-data(:);


	% find peaks
	% note that if just acquire pure sine then need to change the peak detection by jsut removing peakHeight and increasing the distance
	[pks,locs] = findpeaks(data, 'SortStr','descend','MinPeakHeight',std(data)*2.5, 'MinPeakDistance', 400); %store the peak amplitude in pks and the index location of the peaks in locs
	tmpnpks=numel(pks); % temporary store the peak number
	npks=[npks, tmpnpks]; % will be stored iteratively

	% plot the output not necessary
	% figure()
	% x=1:length(data);
	% plot(x,data,x(locs),pks,'or')

	% calculate the mean of pks
	mpks=mean(pks); % temporary store the peak mean
	rpks= [rpks,  mpks]; % will be stored iteratively

end

output=double(horzcat(rstimV', rpks', npks')) %perform horizontal concatenation and conversion to number (aka double)
tang=output(:,2)/2000 % corresponding to a distance of 2000 mm 
angleDeg=atand(tang) % correspond to the angle in degree

% desired deflection is known (200 um) the corresponding voltage to input can be found with 
p = polyfit(output(:,1)', output(:,2)', 1); % output(:,1)'=voltage % output(:,2)'= deflection
p % display the output of he polynomial p(1)=slope p(2)=intercept
f = polyval(p,output(:,1)');
plot(output(:,1)', output(:,2)', 'o', output(:,1)', f, '-')

% equation y=deflection x=voltage - y=p(1)x+p(2)
%desiredDeflection=200
inputVolt = (desiredDeflection - p(2))/p(1)

% corresponding angle in degree can be found with 
p = polyfit(output(:,1)', angleDeg', 1); % output(:,1)'=voltage % output(:,2)'= deflection
finalAngle= inputVolt*p(1)+p(2)


exportData=table(["desiredDeflection";"inputVolt";"finalAngle"],[desiredDeflection;inputVolt;finalAngle]) % careful in matlab "" different from '' and , diffrent form ;


writetable(exportData)
type 'exportData.txt'
close all; clear all