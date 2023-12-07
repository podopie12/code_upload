% This script (or function) was created using MathWorks' MATLAB software.
% Copying, modifying, distributing, or using this code for commercial purposes
% without explicit permission from WooYeongSik is prohibited.

% Copyright (c) [2023] WooYeongSik, Inc.
% Reproduction and use of this code are subject to the MathWorks software

% 폴더 경로 및 이름 정의
function [] = lpf_img(folder_name)


disp('matlab image preprocessing started');

% N by N cut
N = 6;

%inputFolder = folder_name;  % 원본 이미지가 있는 폴더 경로
inputFolder = 'Target_folder';

% 필터 적용된 이미지를 저장할 폴더 이름
outputFolder = sprintf('cut_%d',N*N);

% 폴더가 이미 존재하는지 확인하고 있다면 삭제
if exist(outputFolder, 'dir')
    rmdir(outputFolder, 's');
end

% 폴더 생성
if ~exist(outputFolder, 'dir')
    mkdir(outputFolder);
end


% 폴더 내의 모든 이미지 파일을 처리
imageFiles = dir(fullfile(inputFolder, '*.png'));  % 이미지 파일 형식에 따라 수정

targetSize = [224, 224];

for i = 1:length(imageFiles)
    % 이미지 로딩
    originalImage = imread(fullfile(inputFolder, imageFiles(i).name));
    
    %이미지 크기 확인
    [rows, cols, ~] = size(originalImage);
    
    %이미지를 36개 영역으로 나눕니다.
    row_point = [0, floor(rows / 6), floor(rows / 6 * 2), floor(rows / 6 * 3), floor(rows / 6 * 4), floor(rows / 6 * 5), rows];
    col_point = [0, floor(cols / 6), floor(cols / 6 * 2), floor(cols / 6 * 3), floor(cols / 6 * 4), floor(cols / 6 * 5), cols];
    
    %이미지처리

    outputFolder_sub = sprintf('%s_cut%d', erase(imageFiles(i).name, '.png'),N*N);

    if exist(sprintf('%s%s%s',outputFolder,'\',outputFolder_sub), 'dir')
        rmdir(sprintf('%s%s%s',outputFolder,'\',outputFolder_sub), 's');
    end

    % 폴더 생성
    if ~exist(sprintf('%s%s%s',outputFolder,'\',outputFolder_sub), 'dir')
        mkdir(sprintf('%s%s%s',outputFolder,'\',outputFolder_sub));
    end
    
    for j = 0 : (N * N - 1)
        %이미지처리
        cutted_image = originalImage(row_point(mod(j, N) + 1) + 1 : row_point(mod(j, N) + 2), col_point(fix(j/N) + 1) + 1 : col_point(fix(j/N) + 2), :);
        
        %이미지 사이즈 조정
        cutted_image_resized = imresize(cutted_image, targetSize);
        
        % 결과 이미지 저장
        outputFileName = sprintf('%s_%d.png', erase(imageFiles(i).name, '.png'), j);  % 이미지 파일 형식에 따라 수정
        imwrite(cutted_image_resized, fullfile(outputFolder,outputFolder_sub, outputFileName));
    end
end   

disp('matlab image preprocessing finished');