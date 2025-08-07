from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, roc_auc_score, confusion_matrix, accuracy_score, recall_score
import statsmodels.api as sm
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib
matplotlib.use('Agg')
import matplotlib.font_manager as fm
import platform

# 한글 폰트 설정
if platform.system() == 'Darwin':  # macOS
    plt.rcParams['font.family'] = 'AppleGothic'
elif platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
else:  # Linux
    plt.rcParams['font.family'] = 'DejaVu Sans'
    
plt.rcParams['axes.unicode_minus'] = False

app = Flask(__name__)

# 데이터 로드 및 전처리
def load_data():
    try:
        df = pd.read_csv("video_games.csv", encoding='unicode_escape')
        return df
    except:
        # 샘플 데이터 생성 (실제 데이터가 없을 경우)
        np.random.seed(42)
        n_samples = 1000
        data = {
            'Console': np.random.choice(['Xbox 360', 'PlayStation 3', 'Nintendo DS', 'Wii'], n_samples),
            'Title': [f'Game_{i}' for i in range(n_samples)],
            'US Sales (millions)': np.random.exponential(0.5, n_samples),
            'Review Score': np.random.normal(75, 15, n_samples).clip(0, 100),
            'YearReleased': np.random.randint(2004, 2011, n_samples),
            'Usedprice': np.random.uniform(10, 50, n_samples),
            'Genre': np.random.choice(['Action', 'Sports', 'Racing', 'Platform', 'Shooter', 'RPG'], n_samples),
            'Action': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
            'Platform': np.random.choice([0, 1], n_samples, p=[0.9, 0.1])
        }
        return pd.DataFrame(data)

df = load_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/project1')
def project1():
    # 프로젝트 1 분석
    sales_by_genre = df.groupby('Genre')['US Sales (millions)'].sum().reset_index()
    avg_sales_by_genre = df.groupby('Genre')['US Sales (millions)'].mean().reset_index()
    
    # 차트 생성
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # 총 매출 차트
    sns.barplot(data=sales_by_genre, x='US Sales (millions)', y='Genre', ax=ax1, palette='viridis')
    ax1.set_title('총 매출별 게임 장르')
    
    # 평균 매출 차트
    sns.barplot(data=avg_sales_by_genre, x='US Sales (millions)', y='Genre', ax=ax2, palette='viridis')
    ax2.set_title('게임당 평균 매출별 장르')
    
    plt.tight_layout()
    
    # 차트를 base64로 인코딩
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', dpi=300)
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return render_template('project1.html', chart_url=chart_url)

@app.route('/project2')
def project2():
    # 프로젝트 2 분석
    platform_games = df[df['Platform'] == 1]
    action_games = df[df['Action'] == 1]
    
    # 신뢰구간 계산
    total_games = len(df)
    num_platform_games = len(platform_games)
    proportion_platform = num_platform_games / total_games
    
    # 부트스트랩 신뢰구간
    n_bootstrap = 1000
    bootstrap_proportions = []
    for _ in range(n_bootstrap):
        sample = df.sample(n=total_games, replace=True)
        prop = len(sample[sample['Platform'] == 1]) / total_games
        bootstrap_proportions.append(prop)
    
    ci_lower = np.percentile(bootstrap_proportions, 2.5)
    ci_upper = np.percentile(bootstrap_proportions, 97.5)
    
    # 가설검정
    median_action = np.median(action_games['US Sales (millions)'])
    median_platform = np.median(platform_games['US Sales (millions)'])
    observed_diff = median_action - median_platform
    
    # 부트스트랩 가설검정
    n_samples = 1000
    bootstrap_diffs = []
    for _ in range(n_samples):
        sample_action = action_games.sample(n=len(action_games), replace=True)
        sample_platform = platform_games.sample(n=len(platform_games), replace=True)
        diff = np.median(sample_action['US Sales (millions)']) - np.median(sample_platform['US Sales (millions)'])
        bootstrap_diffs.append(diff)
    
    p_value = np.sum(np.array(bootstrap_diffs) >= observed_diff) / n_samples
    
    # 차트 생성
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # 신뢰구간 히스토그램
    ax1.hist(bootstrap_proportions, bins=30, alpha=0.7, color='skyblue')
    ax1.axvline(proportion_platform, color='red', linestyle='--', label=f'관찰된 비율: {proportion_platform:.3f}')
    ax1.axvline(ci_lower, color='green', linestyle='--', label=f'95% CI 하한: {ci_lower:.3f}')
    ax1.axvline(ci_upper, color='green', linestyle='--', label=f'95% CI 상한: {ci_upper:.3f}')
    ax1.set_title('Platform 게임 비율의 부트스트랩 분포')
    ax1.set_xlabel('비율')
    ax1.set_ylabel('빈도')
    ax1.legend()
    
    # 가설검정 히스토그램
    ax2.hist(bootstrap_diffs, bins=30, alpha=0.7, color='lightcoral')
    ax2.axvline(observed_diff, color='red', linestyle='--', label=f'관찰된 차이: {observed_diff:.3f}')
    ax2.set_title('Action vs Platform 중앙값 차이의 부트스트랩 분포')
    ax2.set_xlabel('중앙값 차이')
    ax2.set_ylabel('빈도')
    ax2.legend()
    
    plt.tight_layout()
    
    # 차트를 base64로 인코딩
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', dpi=300)
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return render_template('project2.html', 
                         chart_url=chart_url,
                         proportion=proportion_platform,
                         ci_lower=ci_lower,
                         ci_upper=ci_upper,
                         p_value=p_value,
                         observed_diff=observed_diff)

@app.route('/project3')
def project3():
    # 프로젝트 3 분석
    df_cleaned = df[['US Sales (millions)', 'Review Score', 'YearReleased', 'Usedprice']].dropna()
    
    X = df_cleaned.drop(columns=['US Sales (millions)'])
    y = df_cleaned['US Sales (millions)']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 선형회귀
    X_train_sm = sm.add_constant(X_train)
    model_sm = sm.OLS(y_train, X_train_sm).fit()
    
    X_test_sm = sm.add_constant(X_test)
    y_pred = model_sm.predict(X_test_sm)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    # 로지스틱 회귀
    y_train_logistic = (y_train > y_train.mean()).astype(int)
    logit_model = sm.Logit(y_train_logistic, X_train_sm).fit()
    
    y_pred_prob = logit_model.predict(X_train_sm)
    auc = roc_auc_score(y_train_logistic, y_pred_prob)
    
    y_pred_prob_test = logit_model.predict(X_test_sm)
    y_pred_test = (y_pred_prob_test >= 0.5).astype(int)
    y_test_logistic = (y_test > y_train.mean()).astype(int)
    
    cm = confusion_matrix(y_test_logistic, y_pred_test)
    accuracy = accuracy_score(y_test_logistic, y_pred_test)
    sensitivity = recall_score(y_test_logistic, y_pred_test)
    specificity = cm[0, 0] / (cm[0, 0] + cm[0, 1])
    
    # 차트 생성
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # 선형회귀 잔차 플롯
    residuals = y_test - y_pred
    ax1.scatter(y_pred, residuals, alpha=0.6)
    ax1.axhline(y=0, color='red', linestyle='--')
    ax1.set_xlabel('예측값')
    ax1.set_ylabel('잔차')
    ax1.set_title('선형회귀 잔차 vs 예측값')
    
    # 실제 vs 예측
    ax2.scatter(y_test, y_pred, alpha=0.6)
    ax2.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    ax2.set_xlabel('실제값')
    ax2.set_ylabel('예측값')
    ax2.set_title('실제값 vs 예측값')
    
    # ROC 곡선
    from sklearn.metrics import roc_curve
    fpr, tpr, _ = roc_curve(y_train_logistic, y_pred_prob)
    ax3.plot(fpr, tpr, label=f'ROC Curve (AUC = {auc:.3f})')
    ax3.plot([0, 1], [0, 1], 'k--', label='Random')
    ax3.set_xlabel('False Positive Rate')
    ax3.set_ylabel('True Positive Rate')
    ax3.set_title('ROC 곡선')
    ax3.legend()
    
    # 혼동행렬 히트맵
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax4)
    ax4.set_title('혼동행렬')
    ax4.set_xlabel('예측')
    ax4.set_ylabel('실제')
    
    plt.tight_layout()
    
    # 차트를 base64로 인코딩
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', dpi=300)
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return render_template('project3.html',
                         chart_url=chart_url,
                         rmse=rmse,
                         r2=r2,
                         auc=auc,
                         accuracy=accuracy,
                         sensitivity=sensitivity,
                         specificity=specificity)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) 