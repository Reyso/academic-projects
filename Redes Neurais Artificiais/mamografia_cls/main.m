
rng(7);


% Definindo os dados de entrada e saída
inputs = x;  % Substitua com seus dados de entrada
targets = y;    % Substitua com seus dados de saída

% Definindo a divisão dos dados (60% treino, 20% validação, 20% teste)
[trainInd, valInd, testInd] = dividerand(size(inputs, 2), 0.6, 0.2, 0.2);

% Separando os dados
train_inputs = inputs(:, trainInd);
train_targets = targets(:, trainInd);

val_inputs = inputs(:, valInd);
val_targets = targets(:, valInd);

test_inputs = inputs(:, testInd);
test_targets = targets(:, testInd);

% Configurando os parâmetros comuns
hidden_layer_sizes = [5, 10, 15, 30, 60];
num_initializations = 3;

% Inicializando a célula para armazenar acurácias e matrizes de confusão
resultados_por_configuracao = cell(length(hidden_layer_sizes), 2);

% Loop sobre os tamanhos de camada escondida
for i = 1:length(hidden_layer_sizes)
    hidden_neurons = hidden_layer_sizes(i);
    
    % Inicializando vetor para armazenar acurácias para esta configuração
    acc_per_config = zeros(num_initializations, 1);
    
    % Inicializando célula para armazenar matrizes de confusão
    confusion_matrices = cell(num_initializations, 1);
    
    % Loop sobre as inicializações
    for j = 1:num_initializations
        % Criando a rede neural MLP com newff
        net = newff(train_inputs, train_targets, hidden_neurons, {'tansig', 'purelin'}, 'trainlm');
        
        % Configurando parâmetros de treinamento
        net.trainParam.epochs = 1000;      % Número de épocas de treinamento
        net.trainParam.lr = 1e-5;         % Taxa de aprendizado
        
        % Treinando a rede neural
        net = train(net, train_inputs, train_targets);
        
        % Testando a rede neural treinada com dados de teste
        outputs = sim(net, test_inputs);
        
        % Calculando a acurácia
        accuracy = sum(round(outputs) == test_targets) / length(test_targets);
        
        % Calculando a matriz de confusão
        confusion_matrix = confusionmat(round(outputs), test_targets);
        
        % Armazenando acurácia e matriz de confusão
        acc_per_config(j) = accuracy;
        confusion_matrices{j} = confusion_matrix;
    end
    
    % Armazenando o vetor de acurácias e matrizes de confusão na célula
    resultados_por_configuracao{i, 1} = acc_per_config;
    resultados_por_configuracao{i, 2} = confusion_matrices;
end

% Exibindo as acurácias e matrizes de confusão
for i = 1:length(hidden_layer_sizes)
    disp(['Resultados para ', num2str(hidden_layer_sizes(i)), ' neurônios na camada escondida:']);
    
    % Exibindo acurácias
    disp('Acurácias:');
    disp(resultados_por_configuracao{i, 1});
    
    % % Exibindo matrizes de confusão
    % disp('Matrizes de Confusão:');
    % for j = 1:num_initializations
    %     disp(['Inicialização ', num2str(j)]);
    %     disp(resultados_por_configuracao{i, 2}{j});
    % end
end
