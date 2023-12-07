%% 5. User place


% 변수 불러오기
load('image_processing.mat');

% 파라미터 정의
folder_name = 'cut_36'; % 이미지가 있는 폴더 이름
scores = [0, 1]; % 각 클래스에 대한 점수
fit_result = [0.988844799693939, -0.238953016150];

% 폴더 내의 모든 서브 폴더를 처리
subFolders = dir(folder_name); 
subFolders = subFolders([subFolders.isdir]);
subFolders = subFolders(~ismember({subFolders.name},{'.','..'})); % '.' 과 '..' 제거

% 클래스 이름
classNames = netTransfer_vgg19.Layers(end).ClassNames;

% 각 서브 폴더에 대해 예측 및 점수 계산
ai_scores = zeros(1, length(subFolders)); % AI 모델을 통해 얻은 점수를 저장할 배열

for i = 1:length(subFolders)

    % 서브 폴더 내의 모든 이미지 파일을 처리
    imageFiles = dir(fullfile(folder_name, subFolders(i).name, '*.png')); % 이미지 파일 형식에 따라 수정
    
    sub_scores = zeros(1, length(imageFiles)); % 각 이미지에 대한 점수를 저장할 배열

    for j = 1:length(imageFiles)

        % 이미지 로딩 및 크기 조정
        testImage = imread(fullfile(folder_name, subFolders(i).name, imageFiles(j).name));
        testImage = imresize(testImage, [224 224]);

        % 이미지를 네트워크에 전달하여 확률 예측
        YPred = predict(netTransfer_vgg19, testImage);

        % 점수 계산
        sub_scores(j) = sum(YPred .* scores); % AI 모델을 통해 얻은 점수를 저장
    end

    % 폴더별 점수 평균 계산
    ai_scores(i) = mean(sub_scores);
end

tire_life_out = (ai_scores - fit_result(2))/fit_result(1);

% 현재 작업 디렉토리 불러오기
current_directory = pwd;

% 파일 이름 설정
file_name = 'tire_life.txt';

% 파일 경로 및 이름 지정
file_path = fullfile(current_directory, file_name);

% 파일 열기
file_id = fopen(file_path, 'w');

fprintf(file_id, '%.4f\n', tire_life_out);

% 파일 닫기
fclose(file_id);

disp('데이터가 메모장으로 내보내졌습니다.');